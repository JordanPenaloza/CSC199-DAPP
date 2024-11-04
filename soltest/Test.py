from web3 import Web3
import json
import seal  

# Ganache setup
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Verify connection
assert web3.is_connected(), "Failed to connect to Ganache."

# Contract address and ABI (replace with your deployed contract’s address and ABI)
contract_address = "0xYourContractAddressHere"
contract_abi = [
    # ... (Copy and paste the contract ABI here) ...
]

# Connect to contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Account details (Ganache account)
account = "0xYourAccountHere"
private_key = "YourPrivateKeyHere"

# Utility function to retrieve and reconstruct keys from chunks
def get_chunked_key(contract, function_name):
    chunks = []
    index = 0
    while True:
        try:
            chunk = getattr(contract.functions, function_name)(index).call()
            chunks.extend(chunk)
            index += 1
        except:
            break
    key_bytes = b''.join([int(chunk).to_bytes(32, byteorder='big') for chunk in chunks])
    return key_bytes

# Retrieve and reconstruct public key and relinearization keys
public_key_bytes = get_chunked_key(contract, "getPublicKeyChunks")
relin_keys_bytes = [get_chunked_key(contract, "getRelinKeyChunks")]

# Initialize SEAL context and FHE keys
parms = seal.EncryptionParameters(seal.scheme_type.ckks)
poly_modulus_degree = 8192  
parms.set_poly_modulus_degree(poly_modulus_degree)
parms.set_coeff_modulus(seal.CoeffModulus.Create(poly_modulus_degree, [60, 40, 40, 60]))
context = seal.SEALContext(parms)

# Generate and set up necessary keys
keygen = seal.KeyGenerator(context)
public_key = seal.PublicKey()
keygen.create_public_key(public_key)

# Convert loaded key bytes into SEAL keys

# Set up Encryptor, Evaluator, Decryptor, and CKKSEncoder
encryptor = seal.Encryptor(context, public_key)
evaluator = seal.Evaluator(context)
decryptor = seal.Decryptor(context, keygen.secret_key())  # Secret key is needed for decryption
encoder = seal.CKKSEncoder(context)

# Scale parameter for precision
scale = pow(2.0, 40)

# Encrypt values in SEAL
def encrypt_value(value, scale=scale):
    # Encode and encrypt the value
    plaintext = seal.Plaintext()
    encoder.encode(value, scale, plaintext)
    ciphertext = seal.Ciphertext()
    encryptor.encrypt(plaintext, ciphertext)
    return ciphertext.save().hex()

# Store encrypted values on-chain
def store_encrypted_value(value):
    encrypted_value = encrypt_value(value)
    txn = contract.functions.storeEncryptedValue([int(encrypted_value, 16)]).build_transaction({
        'from': account,
        'gas': 3000000,
        'nonce': web3.eth.get_transaction_count(account),
    })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    web3.eth.send_raw_transaction(signed_txn.rawTransaction)

def add_encrypted_values():
    encrypted_value1 = contract.functions.getEncryptedValue(account).call()
    encrypted_value2 = contract.functions.getEncryptedValue(account).call()  # Retrieve again for testing

    # Deserialize encrypted values for homomorphic addition
    ciphertext1 = seal.Ciphertext()
    ciphertext1.load(context, bytes.fromhex(encrypted_value1[0]))
    ciphertext2 = seal.Ciphertext()
    ciphertext2.load(context, bytes.fromhex(encrypted_value2[0]))

    # Perform homomorphic addition
    encrypted_result = seal.Ciphertext()
    evaluator.add(ciphertext1, ciphertext2, encrypted_result)

    # Store the result back on-chain
    encrypted_result_hex = encrypted_result.save().hex()
    txn = contract.functions.storeEncryptedResult([int(encrypted_result_hex, 16)]).build_transaction({
        'from': account,
        'gas': 3000000,
        'nonce': web3.eth.get_transaction_count(account),
    })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Encrypted result stored on-chain.")

# Run the test
store_encrypted_value(10)
add_encrypted_values()
