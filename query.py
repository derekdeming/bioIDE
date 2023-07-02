import sys
import requests

engine = sys.argv[1]
query = sys.argv[2]
response = requests.get(f"http://localhost:8000/?engine={engine}&query={query}")
print(response.text)