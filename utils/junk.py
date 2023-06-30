import concurrent.futures
from typing import Dict, List
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.node_parser import SimpleNodeParser
from llama_index.data_structs import Node
from llama_index.schema import Document
from pathlib import Path
from llama_index import download_loader
from llama_index import Document
import ray
from ray.data import ActorPoolStrategy # to use Actors for parallelization -- map_batches() method


ray.init()

# Step 1: Logic for parsing the files into llama_index documents - in our case it will be in formats of json (subject to change)
def process_paper_data(paper_json):
    '''
    This function takes in a json object and returns a llama_index Document object
    
    :param paper_json: a json object containing the data for a single paper
    :return: a llama_index Document object
    '''
    paper_data = {}

    paper_data['doi'] = paper_json['doi']
    paper_data['title'] = paper_json['title']
    paper_data['authors'] = paper_json['authors'].split('; ')
    paper_data['date'] = paper_json['date']
    paper_data['category'] = paper_json['category']
    paper_data['abstract'] = paper_json['abstract']

    # combining all relevant data from the papers into a single string
    paper_text = f"Title: {paper_data['title']}\nAuthors: {', '.join(paper_data['authors'])}\nDate: {paper_data['date']}\nCategory: {paper_data['category']}\nAbstract: {paper_data['abstract']}"

    # instantiate a Document object from llama_index.schema -- requires a doc_id and text and we will use the doi as the doc_id
    document = Document(doc_id=paper_data['doi'], text=paper_text)

    return document

def convert_documents_into_nodes(documents: Dict[str, Document]) -> Dict[str, Node]:
    '''
    This function takes in a dictionary of documents and returns a dictionary of nodes

    :param documents: a dictionary of documents
    :return: a dictionary of nodes
    '''
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents([document for document in documents.values()])
    return [{"node": node} for node in nodes]

@ray.remote
def process_jsons_parallel(jsons: List[Dict]):
    '''
    This function takes in a list of json objects and returns a list of nodes. Idea is to parallelize the processing of the jsons and the creation of the documents
    
    :param jsons: a list of json objects
    :return: a list of nodes
    '''
    document_results = [process_paper_data(json) for json in jsons]
    nodes = convert_documents_into_nodes({doc.doc_id: doc for doc in document_results})
    return nodes
    
# Embed each node using a local embedding model 
@ray.remote
class EmbedNodes:
    def __init__(self):
        '''
        Use all-mpnet-base-v2 Sentence_transformer.
        This is the default embedding model for LlamaIndex/Langchain.

        Use GPU for embedding and specify a large enough batch size to maximize GPU utilization.
        Remove the "device": "cuda" to use CPU instead.
        '''
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2", 
            model_kwargs={"device": "cuda"},
            encode_kwargs={"device": "cuda", "batch_size": 100}
            )
    
    def __call__(self, node_batch: Dict[str, List[Node]]) -> Dict[str, List[Node]]:
        nodes = node_batch["node"]
        text = [node.text for node in nodes]
        embeddings = self.embedding_model.embed_documents(text)
        assert len(nodes) == len(embeddings)

        for node, embedding in zip(nodes, embeddings):
            node.embedding = embedding
        return {"embedded_nodes": nodes}

def create_ray_dataset_pipeline(jsons: List[Dict]):
    # Create the Ray Dataset pipeline
    ds = ray.data.from_items(jsons)
    
    # Initialize the actor
    embed_nodes_actor = EmbedNodes.remote()

    def embed_nodes(node_batch):
        return ray.get(embed_nodes_actor.__call__.remote(node_batch))

    # Use `map_batches` to specify a batch size to maximize GPU utilization.
    embedded_nodes = ds.map_batches(
        embed_nodes, 
        batch_size=100,
        # There are 4 GPUs in the cluster. Each actor uses 1 GPU. So we want 4 total actors.
        # Set the size of the ActorPool to the number of GPUs in the cluster.
        compute=ActorPoolStrategy(size=1), 
        )
    
    # Step 5: Trigger execution and collect all the embedded nodes.
    ray_docs_nodes = []
    for row in embedded_nodes.iter_rows():
        node = row["embedded_nodes"]
        assert node.embedding is not None
        ray_docs_nodes.append(node)

    return ray_docs_nodes

# HANDLING LOCAL FILES - NOT NEEDED FOR NOW
# Step 0: Logic for loading and parsing the files into llama_index documents.
# UnstructuredReader = download_loader("UnstructuredReader")
# loader = UnstructuredReader()

# def load_and_parse_files(file_row: Dict[str, Path]) -> Dict[str, Document]:
#     documents = []
#     file = file_row["path"]
#     if file.is_dir():
#         return []
#     # Skip all non-html files like png, jpg, etc.
#     if file.suffix.lower() == ".html":
#         loaded_doc = loader.load_data(file=file, split_documents=False)
#         loaded_doc[0].extra_info = {"path": str(file)}
#         documents.extend(loaded_doc)
#     return [{"doc": doc} for doc in documents]

