import os
import subprocess

class PubMed:

    def __init__(self):
        pass

    def esearch(self, query, db='pubmed', sort='Relevance', datetype='EDAT', days=5, format='xml'):
        command = f'esearch -db {db} -query "{query}" -sort "{sort}" -datetype {datetype} -days {days} | efetch -format {format}'
        result = subprocess.check_output(command, shell=True)
        return result.decode('utf-8')

    def efetch(self, ids, db='pubmed', format='xml'):
        command = f'efetch -db {db} -id {",".join(ids)} -format {format}'
        result = subprocess.check_output(command, shell=True)
        return result.decode('utf-8')
