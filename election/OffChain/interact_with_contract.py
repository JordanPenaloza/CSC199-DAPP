from web3 import Web3
from fhe_utils import encrypt_vote, retrieve_encrypted_votes
from seal import SEALContext, CKKSEncoder, Encryptor

# Connection setup
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
contract_address = "ADDRESS HERE"
with open("build/contracts/Election.json") as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Submit an encrypted vote for candidate 1
submit_encrypted_vote(candidate_id=1, vote_value=1, account="ACCOUNT HERE", private_key="PRIVATE KEY HERE")
