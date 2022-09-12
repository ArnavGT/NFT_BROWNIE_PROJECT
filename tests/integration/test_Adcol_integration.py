from brownie import AdvancedCollectible, network
import pytest
import time
from scripts.AdvancedCollectible.helpful_scripts import LOCAL_BLOCKCHAIN_NETWORKS, get_contract, get_account
from scripts.AdvancedCollectible.create_collectible import create_collectible


def test_advancedcollectible_integration():
    # deploy the contract
    # create an NFT
    # get a random breed back
    # Here, the chainlink node calls the call_back function instead of us calling it.
    # So, this time, it would truly be random

    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip("Only for testnet testing")

    # Act
    advanced_collectible, creation_tx = create_collectible()
    time.sleep(60)

    # Assert
    assert advanced_collectible.tokenCounter() > 0
