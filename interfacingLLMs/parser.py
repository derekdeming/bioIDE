from typing import Dict
from pathlib import Path
from llama_index.node_parser import SimpleNodeParser
from llama_index.data_structs import Node
from llama_index.schema import Document
from llama_index import download_loader
from llama_index.schema import Document
from dotenv import load_dotenv
import os

api_key = os.getenv('OPENAI_API_KEY')

# if "OPENAI_API_KEY" not in os.environ:
#     raise RuntimeError("Please add the OPENAI_API_KEY environment variable to run this script. Run the following in your terminal `export OPENAI_API_KEY=...`")


UnstructuredReader = download_loader("UnstructuredReader")
loader = UnstructuredReader()

def load_and_parse_json(json_row: Dict[str, str]) -> Dict[str, Document]:

    required_keys = ['doi', 'abstract', 'authors', 'date', 'category']

    for key in required_keys:
        if key not in json_row or json_row[key] is None:
            raise ValueError(f"Missing or null value for required key: {key}")
    
    doc = Document(
        doc_id=json_row['doi'],
        text=json_row['abstract'],
        metadata={
        "authors": json_row['authors'],
        "date": json_row['date'],
        "category": json_row['category']  
        }
    )
    
    return {'doc': doc}



def convert_documents_into_nodes(documents: Dict[str, Document]) -> Dict[str, Node]:
    '''
    This function takes in a dictionary of documents and returns a dictionary of nodes

    :param documents: a dictionary of documents
    :return: a dictionary of nodes
    '''
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)
    return [{"node": node} for node in nodes]


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
