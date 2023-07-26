from typing import List, Dict, Any
from llama_index.data_structs import Node
from abc import ABC, abstractmethod
from db_wrapper.biorxiv import BiorxivDatabase
from .abstract_pipeline import AbstractPipeline
from utils.parser import convert_documents_into_nodes, load_and_parse_json
from utils.embed_nodes import EmbedNodes
import ray
from ray.data import Dataset, ActorPoolStrategy
from llama_index import VectorStoreIndex


class BiorxivPipeline(AbstractPipeline):
    def __init__(self):
        self.database = BiorxivDatabase()

    async def fetch_data(self, interval: str = None, params: dict = None) -> List[Dict[str, Any]]: 
        if interval is None:
            interval = "2021-06-01/2021-06-05" 
        response = self.database.fetch_details(server="biorxiv", interval=interval, params=params)
        papers = response.json()['collection']
        return papers

    async def process_data(self, data: List[Dict]):
        documents = {paper['doi']: load_and_parse_json(paper) for paper in data}
        print(documents)
        nodes = convert_documents_into_nodes(documents)
        self.nodes = nodes

    async def embed_nodes(self):
        nodes = [node["node"] for node in self.nodes]
        ds = ray.data.from_items([{"node": node['node']} for node in nodes], parallelism=20)
        embedded_nodes = ds.map_batches(
            EmbedNodes, 
            batch_size=1, 
            num_cpus=1,
            num_gpus=None,
            compute=ActorPoolStrategy(size=7), 
        )
        self.nodes = [node["embedded_nodes"] for node in embedded_nodes.iter_rows()]
        return self.nodes
    async def store_data(self, nodes: List[Node], storage_dir: str):
        # Embed nodes 
        embedded_nodes = await self.embed_nodes()
        # Construct index
        index = VectorStoreIndex(embedded_nodes, storage_dir)
        for node in embedded_nodes:
            index.add_document(node.doc_id, node.embedding)
        # Store index
        self.store_index(index, storage_dir)


        def store_index(self, index, storage_dir):
            index.build()