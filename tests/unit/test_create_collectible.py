from brownie import AdvancedCollectible, network
import pytest
from scripts.AdvancedCollectible.helpful_scripts import LOCAL_BLOCKCHAIN_NETWORKS, get_contract, get_account
from scripts.AdvancedCollectible.create_collectible import create_collectible


def test_can_Create_advancedcollectible():
    # deploy the contract
    # create an NFT
    # get a ranom breed back

    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip("Only for local testing")

    # Act
    advanced_collectible, creation_tx = create_collectible()
    request_id = creation_tx.events['requestedCollectible']['requestId']
    random_num = 777
    get_contract('vrf_coordinator').callBackWithRandomness(
        request_id, 777, advanced_collectible.address, {'from': get_account()})

    # Assert
    assert advanced_collectible.tokenCounter() > 0
    assert advanced_collectible.tokenIdToBreed(0) == random_num % 3
