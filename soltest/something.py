from random import getrandbits
from web3 import Web3

# Connect to the blockchain
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

# Corrected contract and account details
contract_address = Web3.to_checksum_address('0x43Ef4Ab5FABedEE25B481Bf5472f56D90772Ae7a')
account = Web3.to_checksum_address('0xD269d757021Ee7531f5DD7DE69BFC8F81F9AA1fE')
private_key = '0x9d5e30fe00d1a5f0fefbd4258b97f1818a27c6b3fa6f99d4a8ee106010ba13af'

# Contract ABI
contract_abi = [
	{
		"inputs": [],
		"name": "getKey",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "keyChunks",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256[]",
				"name": "_chunks",
				"type": "uint256[]"
			}
		],
		"name": "storeKey",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Generate a 2048-bit random key and chunk it
key_bits = 2048
key = getrandbits(key_bits)  # Generate a large random integer for the key

# Convert the key to a hex string and pad to ensure it represents 2048 bits
key_hex = f"{key:0{key_bits // 4}x}"

# Split hex string into chunks of 256 bits (64 hex characters) and convert each to an integer
chunk_size = 256
chunks = [int(key_hex[i:i + chunk_size // 4], 16) for i in range(0, len(key_hex), chunk_size // 4)]

print("Generated key chunks for Solidity storage:", chunks)

# Prepare and send the transaction to store the key in chunks
try:
    # Send transaction to store key chunks in the contract
    transaction = contract.functions.storeKey(chunks).transact({
        'from': account,
        'gas': 3000000,
        'gasPrice': w3.to_wei('30', 'gwei')
    })

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(transaction)
    print("Transaction mined successfully!")
except Exception as e:
    print(f"An error occurred: {e}")

# Step 4: Retrieve the stored key chunks from the contract to verify
try:
    # Call the getKey function to retrieve stored chunks
    stored_chunks = contract.functions.getKey().call()
    print("Stored key chunks retrieved from contract:", stored_chunks)

    # Check if the stored chunks match the original chunks
    if stored_chunks == chunks:
        print("Success: Stored key chunks match the original key chunks!")
    else:
        print("Error: Stored key chunks do not match the original key chunks.")
except Exception as e:
    print(f"An error occurred while retrieving key chunks: {e}")
