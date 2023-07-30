import asyncio
from typing import List, Dict, Any
import ray
from biorxiv import BiorxivDatabase
from parser import load_and_parse_json, convert_documents_into_nodes
from embed_nodes import EmbedNodes
from ray.data import Dataset, ActorPoolStrategy
from llama_index.data_structs import Node

class BioRxivManager:
    def __init__(self):
        self.database = BiorxivDatabase()
        self.embedder = EmbedNodes()

    def fetch_data(self, interval: str = None) -> List[Dict[str, Any]]: 
        if interval is None:
            interval = "2021-06-01/2021-06-05" 
        response = self.database.fetch_details(server="biorxiv", interval=interval)
        papers = response.json()['collection']
        return papers

    def process_data(self, data: List[Dict]):
        documents = {paper['doi']: load_and_parse_json(paper)['doc'] for paper in data}
        self.nodes = convert_documents_into_nodes(list(documents.values()))
        return self.nodes

    async def embed_nodes(self):
        ds = ray.data.from_items([node for node in self.nodes], parallelism=20)  # Changed line
        embedded_nodes = ds.map_batches(
            self.embedder,  # Changed line
            batch_size=1, 
            num_cpus=1,
            num_gpus=None,
            compute=ActorPoolStrategy(size=7), 
        )
        self.nodes = [node["embedded_nodes"] for node in embedded_nodes.iter_rows()]
        return self.nodes


if __name__ == "__main__":
    ray.init()
    manager = BioRxivManager()
    papers = manager.fetch_data(interval="2023-07-01/2023-07-30")
    manager.process_data(papers)  # Process the data and store the nodes in manager.nodes

    loop = asyncio.get_event_loop()
    embedded_nodes = loop.run_until_complete(manager.embed_nodes())  # No need to pass nodes, they're stored in manager.nodes

    print(embedded_nodes)
