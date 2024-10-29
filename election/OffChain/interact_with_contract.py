from web3 import Web3

import json

from fhe_utils import encrypt_vote



# Connect to Ganache

ganache_url = "http://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(ganache_url))



# Load Contract

contract_address = "0x9d796A005fa9C9ddB69aB12Fd74e39ea2766780E"

with open("build/contracts/Election.json") as f:

    contract_json = json.load(f)

    contract_abi = contract_json['abi']

contract = web3.eth.contract(address=contract_address, abi=contract_abi)



def submit_encrypted_vote(candidate_id, vote_value, account, private_key):

    encrypted_vote = encrypt_vote(vote_value)

    encrypted_vote_hex = encrypted_vote.save().hex()

    

    txn = contract.functions.submitEncryptedVote(candidate_id, int(encrypted_vote_hex, 16)).build_transaction({

        'from': account,

        'gas': 2000000,

        'gasPrice': web3.toWei('50', 'gwei'),

        'nonce': web3.eth.get_transaction_count(account),

    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    web3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Vote submitted: Transaction Hash: {tx_hash.hex()}")



def retrieve_encrypted_votes(candidate_id):

    encrypted_votes_raw = contract.functions.getEncryptedVotes(candidate_id).call()

    return [bytes.fromhex(hex(v)[2:]) for v in encrypted_votes_raw]





