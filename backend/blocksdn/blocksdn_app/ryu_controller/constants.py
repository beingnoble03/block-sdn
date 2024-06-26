# Secret constants
# TODO @beingnoble03: Should be moved to .env
INFURA_URL = "https://sepolia.infura.io/v3/594fc018fe12410dbcf7089e01913066"
WALLET_ADDRESS = "0x92D30FD5636fb653803f2A9f3dA54E1A77af24fb"


# Authenticator contract constants
AUTHENTICATOR_ABI = """
[
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "auth_type",
				"type": "uint16"
			},
			{
				"internalType": "bytes32",
				"name": "derived_key",
				"type": "bytes32"
			},
			{
				"internalType": "string",
				"name": "device_id",
				"type": "string"
			}
		],
		"name": "add_Authentication_data",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_nos_operator",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "derived_key",
				"type": "bytes32"
			},
			{
				"internalType": "string",
				"name": "device_id",
				"type": "string"
			}
		],
		"name": "type1_auth",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "derived_key",
				"type": "bytes32"
			},
			{
				"internalType": "string",
				"name": "device_id",
				"type": "string"
			}
		],
		"name": "type2_auth",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
"""
AUTHENTICATOR_CONTRACT_ADDRESS = "0x18DCA589376018e30660C49A2E9d987569FE2a2A"

# TODO @beingnoble03: This private key should be moved to .env
PRIVATE_KEY = "d6c728ed2f829c8f3c6d475a7c442ac4002a7f9fcf0ae3e265cf64afe230c380"

DEVICE_TYPE_MAP = {
    "00:00:00:00:00:01": 0,
    "00:00:00:00:00:02": 1,    
    "00:00:00:00:00:03": 0,
    "00:00:00:00:00:04": 1,
}

RYU_CONTROLLER_WSGI_URL = "http://0.0.0.0:8080/simpleswitch/"