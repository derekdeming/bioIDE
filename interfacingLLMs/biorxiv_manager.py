from biorxiv import BiorxivDatabase
from parser import load_and_parse_json, convert_documents_into_nodes

class BioRxivManager:
    def __init__(self):
        self.database = BiorxivDatabase()

    def fetch_and_parse(self, interval: str = None):
        data = self.database.fetch_data(interval)
        documents = [load_and_parse_json(paper)['doc'] for paper in data]
        nodes = convert_documents_into_nodes(documents)
        return nodes

manager = BioRxivManager()
nodes = manager.fetch_and_parse(interval="2023-07-01/2023-07-30")
# print(nodes)

first_five_nodes = nodes[:5]
for idx, node in enumerate(first_five_nodes):
    print(f"Node {idx+1}:")
    print(node)
    print("--------------------")
    print("--------------------")
print(len(nodes))
    