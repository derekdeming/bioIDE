from biorxiv import BiorxivDatabase
from parser import load_and_parse_json, convert_documents_into_nodes

class BioRxivManager:
    def __init__(self):
        self.database = BiorxivDatabase()

    def fetch_and_parse(self, interval: str = None):
        data = self.database.fetch_data(interval)
        # parse the fetched data into a dictionary of documents
        documents = [load_and_parse_json(paper)['doc'] for paper in data]
        # we convert the documents into a dictionary of nodes
        nodes = convert_documents_into_nodes(documents)
        return nodes

# usage
manager = BioRxivManager()
nodes = manager.fetch_and_parse(interval="2023-07-01/2023-07-30")
# print(nodes)

first_five_nodes = nodes[:5]
for i, node in enumerate(first_five_nodes):
    print(f"Node {i+1}:")
    print(node)
    print("--------------------")
    print("--------------------")
print(len(nodes))
    