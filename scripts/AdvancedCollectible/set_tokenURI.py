from brownie import network, AdvancedCollectible
from scripts.AdvancedCollectible.helpful_scripts import get_account, get_breed, OPENSEA_URL
from scripts.AdvancedCollectible.create_metadata import create_metadata


def main():
    print(f'working on {network.show_active()}')
    advanced_collectible = AdvancedCollectible[-1]
    num_collectibles = advanced_collectible.tokenCounter()
    print(f'You have created {num_collectibles} Token IDs!')
    for token_id in range(num_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith('https://'):
            print(f'Setting Token URI of {token_id}')
            set_token_uri(token_id, advanced_collectible, create_metadata())


def set_token_uri(token_id, nft_contract, token_uri):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, token_uri, {'from': account})
    tx.wait(1)
    print(
        f'Awesome, You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}')

    print('Please Wait up to 20 mins and hit refresh! Thank you!')
