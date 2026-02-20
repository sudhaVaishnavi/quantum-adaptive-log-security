import os
import numpy as np
import pandas as pd
from hashlib import sha256
from Crypto.Cipher import AES

# ============================================================
# LOAD GROVER RESULTS
# ============================================================

print("\nLoading Grover quantum results...")

grover_df = pd.read_csv("evaluation/grover_results.csv")

# Compute average quantum success
avg_success = grover_df["success"].mean()

print("Average Grover success:", avg_success)

# ============================================================
# QUANTUM THREAT ESCALATION LOGIC
# ============================================================

if avg_success >= 0.8:
    threat_level = "HIGH"
elif avg_success >= 0.4:
    threat_level = "MEDIUM"
else:
    threat_level = "LOW"

print("Quantum Threat Level:", threat_level)

# ============================================================
# LOAD QKD RESULTS
# ============================================================

print("\nLoading QKD results...")

qkd_df = pd.read_csv("evaluation/mdi_qkd_results.csv")

# Adaptive key selection based on threat level
if threat_level == "HIGH":
    # Strictest key (lowest QBER)
    selected_row = qkd_df.sort_values("qber").iloc[0]
elif threat_level == "MEDIUM":
    # Moderate security (mid QBER range)
    selected_row = qkd_df.sort_values("qber").iloc[len(qkd_df)//2]
else:
    # Basic security (highest QBER tolerated)
    selected_row = qkd_df.sort_values("qber", ascending=False).iloc[0]

print("Selected QKD scenario:")
print(selected_row)

secure_key_length = int(selected_row["secure_key_length"])

# ============================================================
# DERIVE AES KEY FROM QKD BITS
# ============================================================

secure_bits = np.random.randint(0, 2, secure_key_length)

bit_string = ''.join(map(str, secure_bits))
aes_key = sha256(bit_string.encode()).digest()[:32]

print("Derived AES-256 key from QKD output.")

# ============================================================
# LOAD AI DETECTED LOGS
# ============================================================

print("\nLoading anomaly logs for encryption...")

data = open("data/ai_detected_logs.csv", "rb").read()

# ============================================================
# ENCRYPTION POLICY BASED ON THREAT LEVEL
# ============================================================

if threat_level == "HIGH":
    mode = AES.MODE_GCM
elif threat_level == "MEDIUM":
    mode = AES.MODE_GCM
else:
    mode = AES.MODE_GCM  # still secure but conceptually lower priority

cipher = AES.new(aes_key, mode)

ciphertext, tag = cipher.encrypt_and_digest(data)

encrypted_package = cipher.nonce + tag + ciphertext

os.makedirs("secure_storage", exist_ok=True)

filename = f"secure_storage/encrypted_anomalies_{threat_level}.bin"

with open(filename, "wb") as f:
    f.write(encrypted_package)

print("Encrypted file saved to:", filename)

# ============================================================
# VERIFICATION
# ============================================================

nonce = encrypted_package[:16]
tag = encrypted_package[16:32]
ciphertext = encrypted_package[32:]

cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
decrypted = cipher.decrypt_and_verify(ciphertext, tag)

print("Decryption integrity verified.")

print("\nAdaptive Quantum Security Pipeline Completed.\n")