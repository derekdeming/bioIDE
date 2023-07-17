import requests
import os
import gzip
from xml.etree import ElementTree
import ftplib

class GeoDatabase:
    BASE_URL = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    FTP_ROOT = 'ftp.ncbi.nlm.nih.gov'
    
    def __init__(self, db):
        self.db = db
    
    def esearch(self, term):
        esearch_url = f"{self.BASE_URL}/esearch.fcgi"
        params = {"db": self.db, "term": term, "usehistory": "y"}
        response = requests.get(esearch_url, params=params)
        if response.status_code == 200:
            root = ElementTree.fromstring(response.content)
            count = int(root.find('Count').text)
            WebEnv = root.find('WebEnv').text
            query_key = root.find('QueryKey').text
            return count, WebEnv, query_key
        else:
            response.raise_for_status()

    def efetch(self, WebEnv, query_key, retstart, retmax):
        efetch_url = f"{self.BASE_URL}/efetch.fcgi"
        params = {
            "db": self.db,
            "WebEnv": WebEnv,
            "query_key": query_key,
            "retstart": retstart,
            "retmax": retmax
        }
        response = requests.get(efetch_url, params=params)
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

    def fetch_records(self, term, retmax):
        count, WebEnv, query_key = self.esearch(term)
        for retstart in range(0, count, retmax):
            yield self.efetch(WebEnv, query_key, retstart, retmax)
            
    def download_file(self, filepath, dest):
        ftp = ftplib.FTP(self.FTP_ROOT)
        ftp.login()
        with open(dest, 'wb') as fp:
            ftp.retrbinary(f'RETR {filepath}', fp.write)
        ftp.quit()

    def ftp_connect(self):
        ftp = ftplib.FTP(self.FTP_HOST)
        ftp.login()  # i believe this should assume anonymous login
        return ftp

    def construct_geo_directory(self, accession):
        dir_name = accession[:-3] + 'nnn'
        dir_path = f'{self.FTP_ROOT_DIR}/{accession[0:3]}/{dir_name}/{accession}'
        return dir_path

    def fetch_geo_file(self, ftp, dir_path, file_name, local_path):
        full_path = os.path.join(dir_path, file_name)
        local_file_path = os.path.join(local_path, file_name)
        with open(local_file_path, 'wb') as fp:
            ftp.retrbinary('RETR ' + full_path, fp.write)

    def decompress_file(self, file_path):
        with gzip.open(file_path, 'rb') as f_in:
            with open(file_path[:-3], 'wb') as f_out:
                f_out.write(f_in.read())

    def fetch_study_info(self, study_id):
        # to implement, this depends on we decide to parse the response from the server
        pass

    def fetch_metadata(self, record):
        # to implement, this depends on we decide to parse the response from the server
        pass

    def fetch_summary(self, record):
        # to implement, this depends on we decide to parse the response from the server
        pass

    def fetch_data_files(self, record):
        # this will depend on the specific structure of the GEO database
        pass



def test_geodatabase():
    # Create an instance of GeoDatabase for the 'pubmed' database
    db = GeoDatabase('pubmed')

    # Set the search term and number of records to retrieve
    term = 'adipocytes'  # replace with your search term
    retmax = 10 
    print(f"Fetching records for term '{term}'...")
    for record in db.fetch_records(term, retmax):
        print(record)

    # Connect to FTP - 
    ftp = db.ftp_connect()

    # Construct directory and fetch file
    accession = 'GSE159451'  # replace with your accession
    dir_path = db.construct_geo_directory(accession)
    file_name = accession + '_family.soft.gz'  


    local_path = 'C:\\Users\\derek\\cs_projects\\bioML\\bioIDE\storage'  


    print(f"Fetching file '{file_name}'...")
    db.fetch_geo_file(ftp, dir_path, file_name, local_path)

    print(f"Decompressing file '{file_name}'...")
    file_path = os.path.join(local_path, file_name)
    db.decompress_file(file_path)

    ftp.quit()

    print("All tasks completed.")


# Run the test
# test_geodatabase()