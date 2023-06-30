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
# Embed each node using a local embedding model 
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


