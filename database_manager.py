from db_wrapper.biorxiv import BiorxivDatabase
# add the necessary imports
from pathlib import Path
from llama_index import Document
from llama_index.node_parser import SimpleNodeParser
from llama_index.data_structs import Node
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import ray
from ray.data import ActorPoolStrategy

class DatabaseManager:
    def __init__(self):
        self.databases = {
            "biorxiv": BiorxivDatabase(),
            # "geo": GeoDatabase(),
            # need to add the other databases below this -- will get to this later 
        }
        # initialize the embedding model
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2", 
            model_kwargs={"device": "cpu"},
            encode_kwargs={"device": "cpu", "batch_size": 100}
        )

    # add the method to parse, embed and return a vector index of the data
    def parse_and_embed_data(self, paper_data):
        # convert each paper data (JSON string) to a Document object
        documents = [Document(id=i, data=doc) for i, doc in enumerate(paper_data)]
        parser = SimpleNodeParser()
        nodes = parser.get_nodes_from_documents(documents)
        text = [node.text for node in nodes]
        embeddings = self.embedding_model.embed_documents(text)
        assert len(nodes) == len(embeddings)

        for node, embedding in zip(nodes, embeddings):
            node.embedding = embedding
        return nodes


    def fetch(self, db_name, func_name, *args, **kwargs):
        if db_name not in self.databases:
            raise ValueError(f"No database named {db_name}")

        db = self.databases[db_name]
        func = getattr(db, func_name, None)
        
        if not func:
            raise ValueError(f"No function named {func_name} in {db_name}")
        
        return func(*args, **kwargs)