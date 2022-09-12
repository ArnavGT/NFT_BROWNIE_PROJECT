import os
import requests
from pathlib import Path

# Can use this to upload to ipfs instead of upload_to_ipfs functions

PINATA_BASE_URL = 'https://api.pinata.cloud'
endpoint = '/pinning/pinFileToIPFS'
sample_path = './img/shiba-inu.png'
headers = {
    'pinata_api_key': os.getenv('API_Key'),
    'pinata_secret_api_key': os.getenv('API_Secret')
}
print(headers)


def upload_pinata(filepath):
    filename = filepath.split('/')[-1:][0]
    with Path(filepath).open('rb') as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL+endpoint, files={'file': (filename, image_binary)}, headers=headers)

    ipfs_hash = response.json()['IpfsHash']
    image_uri = f'https://ipfs.io/ipfs/{ipfs_hash}/?filename={filename}'
    return image_uri


def main():
    upload_pinata(sample_path)
