import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Load receiver public key
with open("security/public_key.pem", "rb") as f:
    receiver_public_key = serialization.load_pem_public_key(f.read())

# Generate ephemeral key pair
ephemeral_private_key = ec.generate_private_key(ec.SECP256R1())
ephemeral_public_key = ephemeral_private_key.public_key()

# Derive shared secret
shared_key = ephemeral_private_key.exchange(ec.ECDH(), receiver_public_key)

# Derive AES key
aes_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"log encryption"
).derive(shared_key)

# Read original log file
with open("data/raw_logs.csv", "rb") as f:
    plaintext = f.read()

# Encrypt using AES
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# Save ephemeral public key + IV + ciphertext
with open("data/encrypted_logs.enc", "wb") as f:
    f.write(
        ephemeral_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )
    f.write(iv)
    f.write(ciphertext)

print("Log file encrypted successfully (correct ECC hybrid encryption)")
