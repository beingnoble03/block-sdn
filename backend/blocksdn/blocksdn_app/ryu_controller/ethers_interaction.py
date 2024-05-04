from web3 import Web3
from .constants import *

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def web3_is_connected() -> None:
	res = w3.is_connected()
	print(res)

def string_to_bytes32(s):
    # Convert string to bytes
    byte_string = s.encode('utf-8')

    # Pad the byte string with zeros to make it 32 bytes long
    padded_bytes = byte_string.ljust(32, b'\0')

    return padded_bytes

def register_device() -> str:
	contract_instance = w3.eth.contract(address=AUTHENTICATOR_CONTRACT_ADDRESS, abi=AUTHENTICATOR_ABI)
	print(w3.eth.account)

	data = "69"
	print(string_to_bytes32(data))

	# nonce = w3.eth.getTransactionCount(WALLET_ADDRESS)
	nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)
	call_function = contract_instance.functions.add_Authentication_data(0, string_to_bytes32(data), "macbook").build_transaction({"chainId": w3.eth.chain_id, "from": WALLET_ADDRESS, "nonce": nonce})

	signed_tx = w3.eth.account.sign_transaction(call_function, private_key=PRIVATE_KEY)

	send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

	# Wait for transaction receipt
	tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
	print(tx_receipt) # Optional
	print("Transacion successful")

	return "Oh Yeah"

def auth1() -> str:
	contract_instance = w3.eth.contract(address=AUTHENTICATOR_CONTRACT_ADDRESS, abi=AUTHENTICATOR_ABI)
	print(w3.eth.account)

	data = "69"
	print(string_to_bytes32(data))

	is_authenticated = contract_instance.functions.type1_auth(string_to_bytes32(data), "macbook").call()

	print(is_authenticated) # Optional
	print("Transacion successful")

	return str(is_authenticated)

def auth2() -> str:
	contract_instance = w3.eth.contract(address=AUTHENTICATOR_CONTRACT_ADDRESS, abi=AUTHENTICATOR_ABI)
	print(w3.eth.account)

	data = "69"
	print(string_to_bytes32(data))

	is_authenticated = contract_instance.functions.type2_auth(string_to_bytes32(data), "macbook").call()

	print(is_authenticated) # Optional
	print("Transacion successful")

	return str(is_authenticated)