import argparse
from application_logic.pipeline_factory import get_pipeline
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description='Run bio database pipelines.')
    parser.add_argument('--databases', nargs='+', help='List of databases to use')
    parser.add_argument('--interval', help='Interval to fetch data', default=None)
    parser.add_argument('--storage_dir', help='Directory to store api data', default='./')
    parser.add_argument('--store_only', action='store_true', help='Store the data without processing and embedding')

    args = parser.parse_args()

    for database in args.databases:
        pipeline = get_pipeline(database)
        papers = asyncio.run(pipeline.fetch_data(args.interval))

        storage_dir = os.path.join(args.storage_dir, database)
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        if args.store_only:
            asyncio.run(pipeline.store_data(papers, storage_dir))
        else:
            asyncio.run(pipeline.process_data(papers))
            embedded_nodes = asyncio.run(pipeline.embed_nodes())
            asyncio.run(pipeline.store_data(embedded_nodes, storage_dir))

if __name__ == '__main__':
    main()

    # Run selected pipelines concurrently
    # await asyncio.gather(*(run_pipeline(db) for db in args.databases))
    # asyncio.run(main())








# # from db_wrapper import BiorxivDatabase, EnsemblDatabase, GeoDatabase, UniProtDatabase
# from typing import List
# from pathlib import Path
# from utils.embed_nodes import EmbedNodes
# from utils.parser import convert_documents_into_nodes, load_and_parse_json, convert_documents_into_nodes_pdfs, load_and_parse_files_pdfs
# from database_manager import DatabaseManager
# from llama_index import GPTVectorStoreIndex
# import ray
# from ray.data import Dataset
# from ray.data import ActorPoolStrategy
# import json

# def main():
#     db_manager = DatabaseManager()

#     response  = db_manager.fetch("biorxiv", "fetch_details", server="biorxiv", interval="2021-06-01/2021-06-05")
#     papers = response.json()['collection']

#     # formatting it so that we can process each paper separately and store the resulting Documents in a dictionary
#     documents = {paper['doi']: load_and_parse_json(paper)['doc'] for paper in papers}
#     # print(documents)

#     # call the convert documents to nodes function 
#     biorxiv_nodes = convert_documents_into_nodes(list(documents.values()))
#     # print(biorxiv_nodes)

#     # will start to create the Ray Dataset pipeline here 
#     biorxiv_ds = ray.data.from_items([{"node": node['node']} for node in biorxiv_nodes], parallelism=20)
#     print(biorxiv_ds)


#     # Use `map_batches` to specify a batch size to maximize GPU utilization.
#     # We define `EmbedNodes` as a class instead of a function so we only initialize the embedding model once. 
#     #   This state can be reused for multiple batches.
#     embedded_nodes = biorxiv_ds.map_batches(
#         EmbedNodes, 
#         batch_size=1, 
#         # Use 1 GPU per actor.
#         num_cpus=1,
#         num_gpus=None,
#         # There is 1 gpu on the cluster that I am aware of and 16 cpus. Each actor uses 1 cpu. So we will used 7 total actors.
#         # Set the size of the ActorPool to the number of GPUs or CPUs in the cluster.
#         compute=ActorPoolStrategy(size=7), 
#     )

#     # Trigger execution and collect all the embedded nodes.
#     biorxiv_docs_nodes = []
#     for row in embedded_nodes.iter_rows():
#         node = row["embedded_nodes"]
#         assert node.embedding is not None
#         biorxiv_docs_nodes.append(node)

#     # store the embedded nodes in a local vector store, and persist to disk - not ideal but will work for now
#     print("Storing bioRxiv API embeddings in vector index.")

#     biorxiv_docs_index = GPTVectorStoreIndex(nodes=biorxiv_docs_nodes)
#     biorxiv_docs_index.storage_context.persist(persist_dir="C:\\Users\\derek\\cs_projects\\bioML\\bioIDE\\stored_embeddings\\biorxiv")


#     # # get paths the paths for the locally downloaded documentation.
#     # all_docs_gen = Path("./bio_papers").rglob("*")
#     # all_docs = [{"path": doc.resolve()} for doc in all_docs_gen]

#     # # Create the Ray Dataset pipeline - same as above
#     # local_ds = ray.data.from_items(all_docs)
#     # loaded_docs = local_ds.map_batches(load_and_parse_files_pdfs)
#     # bio_local_paper_nodes = loaded_docs.map_batches(convert_documents_into_nodes)
#     # embedded_nodes = bio_local_paper_nodes.map_batches(
#     #     EmbedNodes, 
#     #     batch_size=1, 
#     #     num_cpus=1,
#     #     num_gpus=None,
#     #     compute=ActorPoolStrategy(size=7), 
#     # )
#     # bio_local_docs_nodes = []
#     # for row in embedded_nodes.iter_rows():
#     #     node = row["embedded_nodes"]
#     #     assert node.embedding is not None
#     #     bio_local_docs_nodes.append(node)

#     # print("Storing Ray Documentation embeddings in vector index.")

#     # bio_local_docs_index = GPTVectorStoreIndex(nodes=bio_local_docs_nodes)
#     # bio_local_docs_index.storage_context.persist(persist_dir="C:\\Users\\derek\\cs_projects\\bioML\\bioIDE\\stored_embeddings\\local_papers")

    
    
#     # db = BiorxivDatabase()

#     # # Fetch details for a given date interval
#     # details = db.fetch_details('biorxiv', '2023-06-01/2023-06-01')
#     # print(details.text)

#     # # Fetch preprint publications for a given date interval
#     # preprints = db.fetch_preprint_publications('biorxiv', '2023-06-01/2023-06-05')
#     # print(preprints)

#     # # Fetch published articles for a given date interval
#     # articles = db.fetch_published_articles('2023-06-01/2023-06-05')
#     # print(articles)
    
# #  -------- DO NOT WORK BECAUSE OF THE API (below) -----------
#     # Fetch summary statistics for a given date interval
#     # stats = db.fetch_summary_statistics('2023-06-01/2023-06-05')
#     # print(stats)

#     # Fetch usage statistics for a given date interval
# #     usage = db.fetch_usage_statistics('2023-06-01/2023-06-05')
# #     print(usage)

# #  -------- DO NOT WORK BECAUSE OF THE API (above) -----------

# # #    ---------------- ENSEMBL API -----------------
#     # ensembl = EnsemblDatabase()
#     # sequence = ensembl.get_sequence_by_id("ENSG00000157764")
#     # gene = ensembl.get_gene_by_id("ENSG00000157764")

#     # print(sequence)
#     # print(gene)


# # ---------------- GEO API -----------------
#     # db = "pubmed"  # example database
#     # term = "breast cancer"  # example term
#     # retmax = 1  # example maximum number of records to retrieve at once

#     # geo = GeoDatabase(db)
#     # for batch in geo.fetch_records(term, retmax):
#     #     print(batch)
    

# # ---------------- PUBMED API -----------------
#     # pubmed = PubMed()

#     # # Search for articles
#     # search_results = pubmed.esearch("OpenAI")
#     # print(search_results)

#     # # Fetch specific articles
#     # fetch_results = pubmed.efetch(['25359968', '26287646'])
#     # print(fetch_results)

# # ---------------- UNIPROT API -----------------
#     # uniprot = UniProtDatabase()

#     # protein0 = uniprot.search_proteins('P21802') -- NOT WORKING
#     # protein1 = uniprot.get_protein_by_accession('P21802')
#     # protein2 = uniprot.get_protein_isoforms_by_accession('P21802')
#     # protein3 = uniprot.get_protein_sequence_by_accession('P21802')
#     # protein4 = uniprot.get_protein_features_by_accession('P21802')
#     # protein5 = uniprot.search_protein_features('insulin')
#     # protein6 = uniprot.get_protein_variants_by_accession('P21802', 'isoform')
#     # protein7 = uniprot.get_proteomics_by_accession('P21802')
#     # protein8 = uniprot.get_antigen_by_accession('P21802')
#     # protein9 = uniprot.get_mutagenesis_by_accession('P21802')


#     # print(protein3)

# if __name__ == '__main__':
#     main()