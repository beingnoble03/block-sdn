from web3 import Web3
from .constants import *

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def web3_is_connected() -> None:
	res = w3.is_connected()
	print(res)

def authenticator_contract_interactor() -> str:
	contract_instance = w3.eth.contract(address=AUTHENTICATOR_CONTRACT_ADDRESS, abi=AUTHENTICATOR_ABI)
	res = contract_instance.functions.getMessageHash(WALLET_ADDRESS, 0, "hello world!", 123).call()
	hex = Web3.keccak(res)
	
	return hex.hex()
