from eth_keys import keys
from web3 import Web3

def web3_is_connected(w3) -> None:
	res = w3.is_connected()
	print(res)

def string_to_bytes32(s: str) -> bytes:
    """
    Converts string to bytes32
    """
    byte_string = s.encode('utf-8')
    padded_bytes = byte_string.ljust(32, b'\0')
    return padded_bytes

# TODO: Check the correct way of generating bytes32 key
def private_to_public_key(private_key: str):
	"""
	Gets bytes32 public key from private key
	"""
	pk = keys.PrivateKey(Web3.to_bytes(hexstr=private_key))
	return Web3.to_bytes(hexstr=str(pk.public_key)[2:])[:32]
	