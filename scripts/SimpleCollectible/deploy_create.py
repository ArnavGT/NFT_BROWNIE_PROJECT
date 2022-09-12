from brownie import accounts, SimpleCollectible
from scripts.SimpleCollectible.helpful_scripts import get_account, FORKED_LOCAL_ENVIRONMENTS


# Create your own URI using the template from the course.
sample_tokenURI = 'https://ipfs.io/ipfs/QmYo39skbQ2pUx9GmaKGsPRWFc2d6SvPbEXe2sS377JFdP?filename=shiba-inu.json'
OPENSEA_URL = 'https://testnets.opensea.io/assets/{}/{}'


def deploy_create():
    account = get_account()
    if not SimpleCollectible:
        SimpleCollectible.deploy({'from': account})
    simple_collectible = SimpleCollectible[-1]
    print(simple_collectible)

    tx = simple_collectible.createCollectible(
        sample_tokenURI, {'from': account})
    tx.wait(1)
    print(
        f"Nice, view your NFT here {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}")
    return simple_collectible


def main():
    deploy_create()
