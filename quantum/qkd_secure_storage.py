import os
import numpy as np
import pandas as pd
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# ============================================================
# LOAD MDI-QKD RESULTS
# ============================================================

print("\nLoading QKD secure key...")

qkd_df = pd.read_csv("evaluation/mdi_qkd_results.csv")

# Select most secure scenario (lowest QBER)
best_row = qkd_df.sort_values("qber").iloc[0]

print("Selected scenario:")
print(best_row)

# ============================================================
# GENERATE FINAL KEY FROM QKD OUTPUT
# ============================================================

secure_key_length = int(best_row["secure_key_length"])

# Simulate extracted secure key bits
secure_bits = np.random.randint(0, 2, secure_key_length)

# Convert bits → bytes
bit_string = ''.join(map(str, secure_bits))
byte_key = sha256(bit_string.encode()).digest()[:32]  # AES-256 key

print("Derived AES-256 key from QKD.")

# ============================================================
# LOAD AI DETECTED LOGS
# ============================================================

print("\nLoading AI anomaly logs...")

data = open("data/ai_detected_logs.csv", "rb").read()

# ============================================================
# AES ENCRYPTION
# ============================================================

cipher = AES.new(byte_key, AES.MODE_GCM)

ciphertext, tag = cipher.encrypt_and_digest(data)

encrypted_package = cipher.nonce + tag + ciphertext

os.makedirs("secure_storage", exist_ok=True)

with open("secure_storage/encrypted_anomalies.bin", "wb") as f:
    f.write(encrypted_package)

print("Encrypted file saved to: secure_storage/encrypted_anomalies.bin")

# ============================================================
# DECRYPTION TEST (Integrity Verification)
# ============================================================

nonce = encrypted_package[:16]
tag = encrypted_package[16:32]
ciphertext = encrypted_package[32:]

cipher = AES.new(byte_key, AES.MODE_GCM, nonce=nonce)

decrypted = cipher.decrypt_and_verify(ciphertext, tag)

with open("secure_storage/decrypted_test.csv", "wb") as f:
    f.write(decrypted)

print("Decryption verified successfully.")
