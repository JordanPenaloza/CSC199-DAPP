from interact_with_contract import submit_encrypted_vote, retrieve_encrypted_votes

from fhe_utils import tally_votes, decrypt_result, context

from web3 import Web3



# Define your account and private key

account = "ACCOUNT HEX HERE"

private_key = "PRIVATE KEY HERE"



# Submit an encrypted vote for candidate 1

submit_encrypted_vote(candidate_id=1, vote_value=1, account=account, private_key=private_key)



# Retrieve encrypted votes for candidate 1

encrypted_votes_bytes = retrieve_encrypted_votes(candidate_id=1)



# Convert retrieved bytes into SEAL ciphertexts

from seal import Ciphertext

encrypted_votes = []

for ev in encrypted_votes_bytes:

    ciphertext = Ciphertext()

    ciphertext.load(context, ev)

    encrypted_votes.append(ciphertext)



# Tally the encrypted votes and decrypt the result

encrypted_sum = tally_votes(encrypted_votes)

result = decrypt_result(encrypted_sum)

print(f"Decrypted vote count for candidate 1: {round(result)}")

