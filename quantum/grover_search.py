import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil, log2, pi, sqrt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


# ============================================================
# LOAD AI DETECTED ANOMALIES (LIMITED FOR STABLE SIMULATION)
# ============================================================

print("\nLoading AI detected anomalies...")

df_logs = pd.read_csv("data/ai_detected_logs.csv").head(512)

N = len(df_logs)

print("Total anomalies used:", N)

n = int(ceil(log2(N)))

print("Qubits required:", n)
print("Quantum search space:", 2**n)


# ============================================================
# TARGET SELECTION
# ============================================================

target_random = np.random.randint(0, N)

if 'anomaly_score' in df_logs.columns:
    target_max = df_logs['anomaly_score'].idxmax()
else:
    target_max = 0

target_pattern = 0

targets = list(set([
    target_random,
    target_max,
    target_pattern
]))

targets_binary = [format(t, f'0{n}b')[::-1] for t in targets]

print("Targets selected:", targets)
print("Binary targets:", targets_binary)


# ============================================================
# OUTPUT DIRECTORY
# ============================================================

os.makedirs("evaluation", exist_ok=True)

csv_main   = "evaluation/grover_results.csv"
csv_noise  = "evaluation/grover_noise_results.csv"
plot_main  = "evaluation/grover_success_plot.png"
plot_noise = "evaluation/grover_noise_plot.png"


# ============================================================
# BACKENDS
# ============================================================

ideal_backend = AerSimulator()

noise_model = NoiseModel()

err1 = depolarizing_error(0.002, 1)
err2 = depolarizing_error(0.01, 2)

noise_model.add_all_qubit_quantum_error(err1, ['h', 'x'])
noise_model.add_all_qubit_quantum_error(err2, ['cx'])

noisy_backend = AerSimulator(noise_model=noise_model)

base_shots = 2048
finite_shots = [256, 512, 1024, 2048]


# ============================================================
# ORACLE
# ============================================================

def oracle(qc, target):

    for i, bit in enumerate(target):
        if bit == '0':
            qc.x(i)

    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)

    for i, bit in enumerate(target):
        if bit == '0':
            qc.x(i)


# ============================================================
# DIFFUSER
# ============================================================

def diffuser(qc):

    qc.h(range(n))
    qc.x(range(n))

    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)

    qc.x(range(n))
    qc.h(range(n))


# ============================================================
# GROVER CIRCUIT
# ============================================================

def build_grover_circuit(target):

    qc = QuantumCircuit(n, n)

    qc.h(range(n))

    iterations = int(pi/4 * sqrt(N))

    for _ in range(iterations):
        oracle(qc, target)
        diffuser(qc)

    qc.measure(range(n), range(n))

    return qc, iterations


# ============================================================
# RUN FUNCTION
# ============================================================

def run(qc, backend, shots):

    tqc = transpile(qc, backend)

    depth = tqc.depth()

    job = backend.run(tqc, shots=shots)

    counts = job.result().get_counts()

    return counts, depth


# ============================================================
# EXECUTION
# ============================================================

results = []
noise_results = []

print("\nRunning Grover search...\n")

for s in targets_binary:

    print("Processing target:", s)

    qc, iterations = build_grover_circuit(s)

    counts, depth = run(qc, ideal_backend, base_shots)

    success = counts.get(s, 0) / base_shots

    results.append({
        "target": s,
        "iterations": iterations,
        "success": success,
        "depth": depth
    })

    for shots in finite_shots:

        qc_noise, _ = build_grover_circuit(s)

        counts_noise, _ = run(qc_noise, noisy_backend, shots)

        success_noise = counts_noise.get(s, 0) / shots

        noise_results.append({
            "target": s,
            "shots": shots,
            "success": success_noise
        })


# ============================================================
# SAVE RESULTS
# ============================================================

df1 = pd.DataFrame(results)
df1.to_csv(csv_main, index=False)

df2 = pd.DataFrame(noise_results)
df2.to_csv(csv_noise, index=False)

print("\nSaved:", csv_main)
print("Saved:", csv_noise)


# ============================================================
# PLOT IDEAL SUCCESS
# ============================================================

plt.figure()

plt.bar(df1["target"], df1["success"])

plt.title("Grover Success Probability (Ideal)")
plt.xlabel("Target state")
plt.ylabel("Success")

plt.tight_layout()
plt.savefig(plot_main)
plt.close()

print("Saved:", plot_main)


# ============================================================
# PLOT NOISE PERFORMANCE
# ============================================================

plt.figure()

for t in df2["target"].unique():

    sub = df2[df2["target"] == t]

    plt.plot(sub["shots"], sub["success"], marker="o", label=t)

plt.xscale("log", base=2)

plt.xlabel("Shots")
plt.ylabel("Success")
plt.title("Grover Performance Under Noise")

plt.legend()

plt.tight_layout()
plt.savefig(plot_noise)
plt.close()

print("Saved:", plot_noise)

print("\nGrover layer completed successfully.\n")