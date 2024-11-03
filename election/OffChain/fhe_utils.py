import seal
from web3 import Web3

# --- Initialization and Key Retrieval ---

def get_key_from_chunks(contract, key_type="publicKey"):
    if key_type == "publicKey":
        key_chunks = contract.functions.getPublicKeyChunks().call()
    elif key_type == "relinKey":
        key_chunks = []
        index = 0
        while True:
            try:
                chunk = contract.functions.getRelinKeyChunks(index).call()
                key_chunks.extend(chunk)
                index += 1
            except:
                break

    key_bytes = b''.join([int(chunk).to_bytes(32, byteorder='big') for chunk in key_chunks])
    return key_bytes

# --- Voting Functions ---

def encrypt_vote(encoder, encryptor, vote_value, scale):
    """Encrypt a single vote"""
    plaintext = encoder.encode(vote_value, scale)
    encrypted_vote = encryptor.encrypt(plaintext)
    return encrypted_vote

def tally_votes(evaluator, encrypted_votes):
    """Homomorphically add all encrypted votes"""
    encrypted_sum = encrypted_votes[0]
    for ev in encrypted_votes[1:]:
        evaluator.add_inplace(encrypted_sum, ev)
    return encrypted_sum

def decrypt_result(decryptor, encoder, encrypted_result):
    """Decrypt the aggregated result and decode it"""
    decrypted = decryptor.decrypt(encrypted_result)
    result = encoder.decode(decrypted)
    return result[0]
