from typing import Dict, List
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.data_structs import Node
    
    
class EmbedNodes:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2", 
            model_kwargs={"device": "cpu"},
            encode_kwargs={"device": "cpu", "batch_size": 100}
            )
    
    def __call__(self, node_batch: List[Node]) -> List[Dict[str, Node]]:  # updated input type hint
        # Debug check
        if not all(isinstance(item, Node) for item in node_batch):  # updated condition
            raise ValueError("node_batch should be a list of TextNode instances")

        text = [node.text for node in node_batch]
        embeddings = self.embedding_model.embed_documents(text)
        assert len(node_batch) == len(embeddings)

        for node, embedding in zip(node_batch, embeddings):
            node.embedding = embedding
        return [{"node": node} for node in node_batch]  # return 'node' as key for each node


