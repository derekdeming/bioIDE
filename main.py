from db_wrapper import BiorxivDatabase, EnsemblDatabase, GeoDatabase, UniProtDatabase
from db_wrapper.pubmed import PubMed



def main():
    
    #    ---------------- BIORXIV API -----------------
    # db = BiorxivDatabase()

    # # Fetch details for a given date interval
    # details = db.fetch_details('biorxiv', '2023-06-01/2023-06-05')
    # print(details)

    # # Fetch preprint publications for a given date interval
    # preprints = db.fetch_preprint_publications('biorxiv', '2023-06-01/2023-06-05')
    # print(preprints)

    # # Fetch published articles for a given date interval
    # articles = db.fetch_published_articles('2023-06-01/2023-06-05')
    # print(articles)
    
#  -------- DO NOT WORK BECAUSE OF THE API (below) -----------
    # Fetch summary statistics for a given date interval
    # stats = db.fetch_summary_statistics('2023-06-01/2023-06-05')
    # print(stats)

    # Fetch usage statistics for a given date interval
#     usage = db.fetch_usage_statistics('2023-06-01/2023-06-05')
#     print(usage)

#  -------- DO NOT WORK BECAUSE OF THE API (above) -----------

# #    ---------------- ENSEMBL API -----------------
    # ensembl = EnsemblDatabase()
    # sequence = ensembl.get_sequence_by_id("ENSG00000157764")
    # gene = ensembl.get_gene_by_id("ENSG00000157764")

    # print(sequence)
    # print(gene)


# ---------------- GEO API -----------------
    # db = "pubmed"  # example database
    # term = "breast cancer"  # example term
    # retmax = 1  # example maximum number of records to retrieve at once

    # geo = GeoDatabase(db)
    # for batch in geo.fetch_records(term, retmax):
    #     print(batch)
    

# ---------------- PUBMED API -----------------
    # pubmed = PubMed()

    # # Search for articles
    # search_results = pubmed.esearch("OpenAI")
    # print(search_results)

    # # Fetch specific articles
    # fetch_results = pubmed.efetch(['25359968', '26287646'])
    # print(fetch_results)

# ---------------- UNIPROT API -----------------
    uniprot = UniProtDatabase()

    # protein0 = uniprot.search_proteins('P21802') -- NOT WORKING
    # protein1 = uniprot.get_protein_by_accession('P21802')
    # protein2 = uniprot.get_protein_isoforms_by_accession('P21802')
    # protein3 = uniprot.get_protein_sequence_by_accession('P21802')
    # protein4 = uniprot.get_protein_features_by_accession('P21802')
    # protein5 = uniprot.search_protein_features('insulin')
    # protein6 = uniprot.get_protein_variants_by_accession('P21802', 'isoform')
    # protein7 = uniprot.get_proteomics_by_accession('P21802')
    # protein8 = uniprot.get_antigen_by_accession('P21802')
    protein9 = uniprot.get_mutagenesis_by_accession('P21802')


    print(protein9)

if __name__ == '__main__':
    main()