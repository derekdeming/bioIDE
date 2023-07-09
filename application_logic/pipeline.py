from application_logic.pipelines.biorxiv_pipeline import BiorxivPipeline
import asyncio
from llama_index import GPTVectorStoreIndex

async def run_pipeline(database_name: str, interval: str = None):

    pipeline = get_pipeline(database_name)

    papers = await pipeline.fetch_data(interval)
    await pipeline.process_data(papers)
    embedded_nodes = await pipeline.embed_nodes()

    print(f"Storing {type(pipeline).__name__} embeddings in vector index.")
    docs_index = GPTVectorStoreIndex(nodes=embedded_nodes)
    docs_index.storage_context.persist(persist_dir=f"C:\\Users\\derek\\cs_projects\\bioML\\bioIDE\\database_storage\\stored_embeddings\\{type(pipeline).__name__}")

def get_pipeline(database_name: str):
    # Map database names to pipeline classes
    pipeline_classes = {
        'biorxiv': BiorxivPipeline,
        # 'pubmed': PubmedPipeline,
        # 'geo': GeoPipeline,
        # 'ensembl': EnsemblPipeline,
        # ....
    }

    pipeline_class = pipeline_classes.get(database_name.lower())

    if pipeline_class is None:
        raise ValueError(f"Unknown database: {database_name}")
    
    return pipeline_class()