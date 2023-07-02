from typing import Dict, List
from pathlib import Path
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.node_parser import SimpleNodeParser
from llama_index.data_structs import Node
from llama_index.schema import Document
from llama_index import download_loader
from llama_index.schema import Document


import os
if "OPENAI_API_KEY" not in os.environ:
    raise RuntimeError("Please add the OPENAI_API_KEY environment variable to run this script. Run the following in your terminal `export OPENAI_API_KEY=...`")


UnstructuredReader = download_loader("UnstructuredReader")
loader = UnstructuredReader()

def load_and_parse_json(json_row: Dict[str, str]) -> Dict[str, Document]:
    """
    Parse a row of JSON data into a Document object.

    Args:
        json_row (Dict[str, str]): A row of JSON data.

    Returns:
        Dict[str, Document]: A dictionary containing a "doc" key and a Document value.
    """
    required_keys = ['doi', 'abstract', 'authors', 'date', 'category']
    for key in required_keys:
        if key not in json_row or json_row[key] is None:
            raise ValueError(f"Missing or null value for required key: {key}")
    
    doc = Document(
        doc_id=json_row.get('doi'),
        text=json_row.get('abstract'),
        extra_info={"authors": json_row.get('authors'), "date": json_row.get('date'), "category": json_row.get('category')}
    )
    return {"doc": doc}


def convert_documents_into_nodes(documents: Dict[str, Document]) -> Dict[str, Node]:
    '''
    This function takes in a dictionary of documents and returns a dictionary of nodes

    :param documents: a dictionary of documents
    :return: a dictionary of nodes
    '''
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)
    return [{"node": node} for node in nodes]


class EmbedNodes:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            # Use all-mpnet-base-v2 Sentence_transformer.
            # This is the default embedding model for LlamaIndex/Langchain.
            model_name="sentence-transformers/all-mpnet-base-v2", 
            model_kwargs={"device": "cpu"},
            # Use GPU for embedding and specify a large enough batch size to maximize GPU utilization.
            # Remove the "device": "cuda" to use CPU instead.
            encode_kwargs={"device": "cpu", "batch_size": 100}
            )
    
    def __call__(self, node_batch: Dict[str, List[Node]]) -> Dict[str, List[Node]]:
        nodes = node_batch["node"]
        text = [node.text for node in nodes]
        embeddings = self.embedding_model.embed_documents(text)
        assert len(nodes) == len(embeddings)

        for node, embedding in zip(nodes, embeddings):
            node.embedding = embedding
        return {"embedded_nodes": nodes}


def load_and_parse_files_pdfs(file_row: Dict[str, Path]) -> Dict[str, Document]:
    documents = []
    file = Path(file_row["path"].item())
    if file.is_dir():
        return []
    # Skip all non-html files like png, jpg, etc.
    if file.suffix.lower() == ".pdf":
        loaded_doc = loader.load_data(file=file, split_documents=False)
        loaded_doc[0].extra_info = {"path": str(file)}
        documents.extend(loaded_doc)
    return [{"doc": doc} for doc in documents]


def convert_documents_into_nodes_pdfs(documents: Dict[str, Document]) -> Dict[str, Node]:
    parser = SimpleNodeParser()
    document = documents["doc"]
    nodes = parser.get_nodes_from_documents([document])
    return [{"node": node} for node in nodes]


















# # Get the paths for the locally downloaded documentation.
# all_docs_gen = Path("../bio_papers").rglob("*")
# all_docs = [{"path": doc.resolve()} for doc in all_docs_gen]

# # Create the Ray Dataset pipeline
# ds = ray.data.from_items(all_docs)
# # Use `flat_map` since there is a 1:N relationship. Each filepath returns multiple documents.
# loaded_docs = ds.map_batches(load_and_parse_files)
# # Use `flat_map` since there is a 1:N relationship. Each document returns multiple nodes.
# nodes = loaded_docs.map_batches(convert_documents_into_nodes)
# # Use `map_batches` to specify a batch size to maximize GPU utilization.
# # We define `EmbedNodes` as a class instead of a function so we only initialize the embedding model once. 
# #   This state can be reused for multiple batches.
# embedded_nodes = nodes.map_batches(
#     EmbedNodes, 
#     batch_size=100, 
#     # Use 1 GPU per actor.
#     num_gpus=1,
#     # There are 4 GPUs in the cluster. Each actor uses 1 GPU. So we want 4 total actors.
#     # Set the size of the ActorPool to the number of GPUs in the cluster.
#     compute=ActorPoolStrategy(size=1), 
#     )


# # Step 5: Trigger execution and collect all the embedded nodes.
# bio_docs_nodes = []
# for row in embedded_nodes.iter_rows():
#     node = row["embedded_nodes"]
#     assert node.embedding is not None
#     bio_docs_nodes.append(node)

# # Step 6: Store the embedded nodes in a local vector store, and persist to disk.
# print("Storing Ray Documentation embeddings in vector index.")

# bio_docs_index = GPTVectorStoreIndex(nodes=bio_docs_nodes)
# bio_docs_index.storage_context.persist(persist_dir="/tmp/bio_docs_index")





























# Repeat the same steps for the Anyscale blogs
# Download the Anyscale blogs locally
# all_blogs_gen = Path("./www.anyscale.com/blog/").rglob("*")
# all_blogs = [{"path": blog.resolve()} for blog in all_blogs_gen]

# ds = ray.data.from_items(all_blogs)
# loaded_docs = ds.flat_map(load_and_parse_files)
# nodes = loaded_docs.flat_map(convert_documents_into_nodes)
# embedded_nodes = nodes.map_batches(
#     EmbedNodes, 
#     batch_size=100, 
#     compute=ActorPoolStrategy(size=4), 
#     num_gpus=1)





