import concurrent.futures
from typing import Dict, List
from llama_index.node_parser import SimpleNodeParser
from llama_index.data_structs import Node
from llama_index.schema import Document

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

def process_jsons_parallel(jsons: List[Dict]):
    '''
    This function takes in a list of json objects and returns a list of nodes. Idea is to parallelize the processing of the jsons and the creation of the documents
    
    :param jsons: a list of json objects
    :return: a list of nodes
    '''
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # parallelizing the JSON processing and Document creation
        document_results = list(executor.map(process_paper_data, jsons))

        # converting the documents into nodes in parallel
        nodes = convert_documents_into_nodes({doc.doc_id: doc for doc in document_results})

        return nodes
    

