from abc import ABC, abstractmethod
from typing import Dict, List
from llama_index.data_structs import Node

class AbstractPipeline(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def fetch_data(self, interval: str) -> List[Dict]:
        pass

    @abstractmethod
    def process_data(self, data: List[Dict]) -> List[Node]:
        pass

    @abstractmethod
    def embed_nodes(self, nodes: List[Node]) -> List[Node]:
        pass
