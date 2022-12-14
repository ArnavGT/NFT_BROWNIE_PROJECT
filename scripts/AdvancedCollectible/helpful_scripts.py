from brownie import accounts, network, config, LinkToken, VRFCoordinatorMock, Contract
from web3 import Web3

DECIMALS = 8  # this will be 18 for normal developemnt chiains, its 8 now because fundme had only 8 decimals
STARTING_PRICE = Web3.toWei(1672.83, 'ether')

LOCAL_BLOCKCHAIN_NETWORKS = ['development', 'ganache-local', 'mainnet-fork']
FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork']
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_account(index=None, id=None):
    if network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    if index:
        return accounts[index]
    if id:
        return accounts.add(id)
    return accounts.add(config['wallets']['from_key'])


contract_to_mock = {"link_token": LinkToken,
                    "vrf_coordinator": VRFCoordinatorMock}


def get_contract(contract_name):
    """
    This function will either:
        - Get an address from the config
        - Or deploy a Mock to use for a network that doesn't have the contract
    Args:
        contract_name (string): This is the name of the contract that we will get
        from the config or deploy
    Returns:
        brownie.network.contract.ProjectContract: This is the most recently deployed
        Contract of the type specified by a dictionary. This could either be a mock
        or a 'real' contract on a live network.
    """
    # link_token
    # LinkToken
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active(
        )][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def fund_with_link(contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, 'ether')):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract('link_token')
    funding_tx = link_token.transfer(
        contract_address, amount, {'from': account})
    funding_tx.wait(1)
    print(f"Funded Link to {contract_address}")
    return funding_tx


def deploy_mocks():
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    account = get_account()
    print("Deploying Mock LinkToken...")
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token deployed to {link_token.address}")
    print("Deploying Mock VRF Coordinator...")
    vrf_coordinator = VRFCoordinatorMock.deploy(
        link_token.address, {"from": account})
    print(f"VRFCoordinator deployed to {vrf_coordinator.address}")
    print("All done!")


def get_breed(tokenId):
    breeds = ['pug', 'shiba_inu', 'st_bernard']
    return breeds[tokenId]


def get_pf_address(feed_type):
    # If we are not in development, use the address for the required network
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pf_address = config['networks'][network.show_active()
                                        ][feed_type]
        return pf_address

    else:  # If we are in develpoment, deploy mocks.
        return deploy_mocks()
