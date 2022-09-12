from brownie import AdvancedCollectible, config, network
from scripts.AdvancedCollectible.helpful_scripts import fund_with_link, get_account, get_contract
from web3 import Web3
from scripts.AdvancedCollectible.set_tokenURI import set_token_uri


def create_collectible():
    account = get_account()
    if not AdvancedCollectible:
        AdvancedCollectible.deploy(get_contract('vrf_coordinator'),
                                   get_contract('link_token'),
                                   config['networks'][network.show_active()
                                                      ]['keyhash'],
                                   config['networks'][network.show_active()
                                                      ]['fee'],
                                   {'from': account})

    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address,
                   amount=Web3.toWei(0.2, "ether"))
    creation_transaction = advanced_collectible.createCollectible({
                                                                  "from": account})
    creation_transaction.wait(1)
    print("Collectible created!")
    return advanced_collectible, creation_transaction


def main():
    create_collectible()
