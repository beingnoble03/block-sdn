from web3 import Web3
from .device_interaction import get_device_type, is_device_valid, inform_device
from .constants import *
from .utils import private_to_public_key

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def register_device(data) -> str:
	contract_instance = w3.eth.contract(address=AUTHENTICATOR_CONTRACT_ADDRESS, abi=AUTHENTICATOR_ABI)

	device_id = data.get("deviceId")

	if not is_device_valid(device_id):
		return "Device Id is not valid"

	private_key = data.get("privKey")
	device_type = get_device_type(device_id)
	public_key = private_to_public_key(private_key)

	nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)
	
	call_function = contract_instance.functions.add_Authentication_data(device_type, public_key, device_id).build_transaction({"chainId": w3.eth.chain_id, "from": WALLET_ADDRESS, "nonce": nonce})

	signed_tx = w3.eth.account.sign_transaction(call_function, private_key=PRIVATE_KEY)

	send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

	tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
	
	if tx_receipt == None:
		return "The device could not be registered"
	
	print(tx_receipt)

	inform_device(device_id)

	return "The device has been registered"

def auth(data) -> str:
	"""
	Simply maps to different authentication methods
	"""
	device_id = data.get("deviceId")

	device_type = get_device_type(device_id)
	if device_type:
		return auth2(data)
	
	return auth1(data)

def auth1(data) -> str:
	# TODO: Ping to host using mininet
	contract_instance = w3.eth.contract(address=AUTHENTICATOR_CONTRACT_ADDRESS, abi=AUTHENTICATOR_ABI)
	
	device_id = data.get("deviceId")
	private_key = data.get("privKey")
	public_key = private_to_public_key(private_key)

	is_authenticated = contract_instance.functions.type1_auth(public_key, device_id).call()

	print(is_authenticated)

	if is_authenticated:
		inform_device(device_id)

	return str(is_authenticated)

def auth2(data) -> str:
	# TODO: Ping to host using mininet
	contract_instance = w3.eth.contract(address=AUTHENTICATOR_CONTRACT_ADDRESS, abi=AUTHENTICATOR_ABI)

	device_id = data.get("deviceId")
	private_key = data.get("privKey")
	public_key = private_to_public_key(private_key)

	is_authenticated = contract_instance.functions.type2_auth(public_key, device_id).call()

	print(is_authenticated)

	if is_authenticated:
		inform_device(device_id)

	return str(is_authenticated)
