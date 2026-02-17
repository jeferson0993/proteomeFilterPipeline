import requests
import os

def download_proteome(proteome_id, output_path):
    url = f"https://rest.uniprot.org/uniprotkb/stream?format=fasta&query=proteome:{proteome_id}"
    response = requests.get(url)
    response.raise_for_status()

    with open(output_path, "w") as f:
        f.write(response.text)
