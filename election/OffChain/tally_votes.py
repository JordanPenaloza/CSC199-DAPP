from web3 import Web3
from fhe_utils import setup_fhe_from_contract, tally_votes, decrypt_result, get_key_from_chunks
from seal import SEALContext, CKKSEncoder, Evaluator, Encryptor, Decryptor, Ciphertext

# Connect to Ganache and the contract
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
contract_address = "ADDRESS HERE"
with open("build/contracts/Election.json") as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Retrieve FHE keys from contract
public_key_bytes = get_key_from_chunks(contract, "publicKey")
relin_key_bytes = get_key_from_chunks(contract, "relinKey")

# Initialize SEAL with retrieved keys and parameters
context, public_key, relin_keys, encoder, evaluator = setup_fhe_from_contract(contract)

# Voting and tallying
encrypted_votes = retrieve_encrypted_votes(candidate_id=1)
encrypted_sum = tally_votes(evaluator, encrypted_votes)
result = decrypt_result(decryptor, encoder, encrypted_sum)
print(f"Decrypted vote count for candidate 1: {round(result)}")
