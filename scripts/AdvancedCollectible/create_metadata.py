import json
import os
from brownie import AdvancedCollectible, network
from scripts.AdvancedCollectible.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
#import requests
from scripts.AdvancedCollectible.upload_to_pinata import upload_pinata


breed_to_imageUri = {
    'pug': 'https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8/?filename=1-pug.json',
    'shiba_inu': 'https://ipfs.io/ipfs/QmYZpR7UysBhhGATsAPeynugLtHf7xno9LU8mVY87wCE1T/?filename=0-shiba_inu.json',
    'st_bernard': 'https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.json'
}


def create_metadata():
    advanced_collectible = AdvancedCollectible[-1]
    num_collectibles = advanced_collectible.tokenCounter()
    print(f'You have created {num_collectibles} collectibles!')

    for tokenId in range(num_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(tokenId))
        metadata_filename = (
            f"./metadata/{network.show_active()}/{tokenId}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_filename).exists():
            print(f'{metadata_filename} already exists! Delete it to overwrite.')
        else:
            print(f'Creating Metadata file {metadata_filename}')
            collectible_metadata['name'] = breed
            collectible_metadata['description'] = f'An Adorable {breed} pup!'
            image_path = './img/' + breed.lower().replace('_', '-') + '.png'
            if os.getenv('UPLOAD_IPFS') == 'true':
                image_uri = upload_pinata(image_path)
            image_uri = image_uri if image_uri else breed_to_imageUri[breed]
            collectible_metadata['image'] = image_uri
            with open(metadata_filename, 'w') as file:
                json.dump(collectible_metadata, file)
                print(image_uri)
            if os.getenv('UPLOAD_IPFS') == 'true':
                meta_Data = upload_pinata(metadata_filename)
            return meta_Data


def main():
    create_metadata()

# def upload_to_ipfs(filepath):
#    with Path(filepath).open("rb") as fp:
#        image_binary = fp.read()
#        ipfs_url = "http://127.0.0.1:5001"
#        endpoint = '/api/v0/add'
#        response = requests.post(
#            ipfs_url + endpoint, files={"file": image_binary})
#        ipfs_hash = response.json()['Hash']
#        # "./img/0-shiba-inu.png" -> "0-shiba-inu.png"
#        filename = filepath.split('/')[-1:][0]
#        image_uri = f'https://ipfs.io/ipfs/{ipfs_hash}/?filename={filename}'
#        print(image_uri)
#        return image_uri
