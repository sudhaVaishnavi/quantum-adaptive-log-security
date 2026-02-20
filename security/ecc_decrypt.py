from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Load receiver private key
with open("security/private_key.pem", "rb") as f:
    receiver_private_key = serialization.load_pem_private_key(f.read(), password=None)

# Read encrypted file
with open("data/encrypted_logs.enc", "rb") as f:
    data = f.read()

# Extract ephemeral public key
end_marker = b"-----END PUBLIC KEY-----\n"
end_index = data.find(end_marker) + len(end_marker)

ephemeral_public_key = serialization.load_pem_public_key(data[:end_index])

# Extract IV and ciphertext
iv = data[end_index:end_index+16]
ciphertext = data[end_index+16:]

# Derive shared secret
shared_key = receiver_private_key.exchange(ec.ECDH(), ephemeral_public_key)

# Derive AES key
aes_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"log encryption"
).derive(shared_key)

# Decrypt
cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()

# Save decrypted file
with open("data/decrypted_logs.csv", "wb") as f:
    f.write(plaintext)

print("Log file decrypted successfully (correct ECC hybrid decryption)")
