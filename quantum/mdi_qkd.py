import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# CONFIGURATION
# ============================================================

NUM_BITS = 10000
NOISE_LEVELS = [0.0, 0.02, 0.05, 0.1]
ATTACK_PROBABILITIES = [0.0, 0.1, 0.25, 0.5]

np.random.seed(42)

os.makedirs("evaluation", exist_ok=True)

# ============================================================
# CORE PROTOCOL LOGIC (CORRECTED)
# ============================================================

def generate_bits(n):
    return np.random.randint(0, 2, n)

def generate_bases(n):
    return np.random.randint(0, 2, n)  # 0 = Z, 1 = X

def apply_noise(bits, noise_level):
    flip_mask = np.random.rand(len(bits)) < noise_level
    noisy = np.copy(bits)
    noisy[flip_mask] ^= 1
    return noisy

def intercept_resend_attack(bits, attack_prob):
    attack_mask = np.random.rand(len(bits)) < attack_prob
    attacked = np.copy(bits)
    random_bits = np.random.randint(0, 2, len(bits))
    attacked[attack_mask] = random_bits[attack_mask]
    return attacked

def calculate_qber(a, b):
    return np.sum(a != b) / len(a)

def privacy_amplification(key, qber):
    reduction_factor = max(0, 1 - 2*qber)
    new_length = int(len(key) * reduction_factor)
    return key[:new_length]

# ============================================================
# MDI-QKD SIMULATION
# ============================================================

def run_simulation(noise, attack_prob):

    # Alice prepares bits + bases
    alice_bits = generate_bits(NUM_BITS)
    alice_bases = generate_bases(NUM_BITS)

    # Bob prepares bases
    bob_bases = generate_bases(NUM_BITS)

    # In honest MDI, Bob reconstructs Alice’s bit
    bob_bits = np.copy(alice_bits)

    # Attack occurs before noise
    bob_bits = intercept_resend_attack(bob_bits, attack_prob)

    # Channel noise
    bob_bits = apply_noise(bob_bits, noise)

    # Sifting (keep only matching bases)
    sift_mask = alice_bases == bob_bases

    sifted_alice = alice_bits[sift_mask]
    sifted_bob = bob_bits[sift_mask]

    if len(sifted_alice) == 0:
        return 0, 0, 0

    qber = calculate_qber(sifted_alice, sifted_bob)

    secure_key = privacy_amplification(sifted_alice, qber)

    key_rate = len(secure_key) / NUM_BITS

    return qber, key_rate, len(secure_key)

# ============================================================
# MAIN EXECUTION
# ============================================================

results = []

print("\nRunning Corrected Research-Grade MDI-QKD Simulation...\n")

for noise in NOISE_LEVELS:
    for attack in ATTACK_PROBABILITIES:

        qber, key_rate, key_length = run_simulation(noise, attack)

        print(f"Noise: {noise} | Attack: {attack} | QBER: {qber:.4f} | Key Rate: {key_rate:.4f}")

        results.append({
            "noise": noise,
            "attack_probability": attack,
            "qber": qber,
            "key_rate": key_rate,
            "secure_key_length": key_length
        })

# ============================================================
# SAVE RESULTS
# ============================================================

df = pd.DataFrame(results)
df.to_csv("evaluation/mdi_qkd_results.csv", index=False)

print("\nSaved: evaluation/mdi_qkd_results.csv")

# ============================================================
# PLOT QBER
# ============================================================

plt.figure()

for noise in NOISE_LEVELS:
    subset = df[df["noise"] == noise]
    plt.plot(subset["attack_probability"], subset["qber"], marker="o", label=f"Noise={noise}")

plt.xlabel("Attack Probability")
plt.ylabel("QBER")
plt.title("QBER vs Attack Probability (MDI-QKD)")
plt.legend()
plt.tight_layout()
plt.savefig("evaluation/mdi_qkd_qber_plot.png")
plt.close()

print("Saved: evaluation/mdi_qkd_qber_plot.png")

# ============================================================
# PLOT KEY RATE
# ============================================================

plt.figure()

for noise in NOISE_LEVELS:
    subset = df[df["noise"] == noise]
    plt.plot(subset["attack_probability"], subset["key_rate"], marker="o", label=f"Noise={noise}")

plt.xlabel("Attack Probability")
plt.ylabel("Secure Key Rate")
plt.title("Key Rate vs Attack Probability (MDI-QKD)")
plt.legend()
plt.tight_layout()
plt.savefig("evaluation/mdi_qkd_keyrate_plot.png")
plt.close()

print("Saved: evaluation/mdi_qkd_keyrate_plot.png")

print("\nCorrected MDI-QKD Simulation Completed Successfully.\n")