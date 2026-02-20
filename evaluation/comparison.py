import pandas as pd
import matplotlib.pyplot as plt
import os

print("\nLoading classical and quantum results...\n")

classical = pd.read_csv("evaluation/classical_results.csv")
quantum = pd.read_csv("evaluation/grover_results.csv")

# Extract classical metrics
classical_detection = classical["detection_rate"].values[0]
classical_time = classical["execution_time_seconds"].values[0]

# Extract quantum metrics (average success)
quantum_success = quantum["success"].mean()
quantum_depth = quantum["depth"].mean()

print("Classical Detection Rate:", classical_detection)
print("Classical Execution Time:", classical_time)
print("Quantum Average Success:", quantum_success)
print("Quantum Average Circuit Depth:", quantum_depth)

# ============================================================
# CREATE COMPARISON TABLE
# ============================================================

comparison_data = {
    "Metric": [
        "Detection Rate",
        "Execution Time (sec)",
        "Complexity",
        "Circuit Depth"
    ],
    "Classical": [
        classical_detection,
        classical_time,
        "O(N)",
        "-"
    ],
    "Quantum": [
        quantum_success,
        "Theoretical O(√N)",
        "O(√N)",
        quantum_depth
    ]
}

df_compare = pd.DataFrame(comparison_data)

df_compare.to_csv("evaluation/final_comparison.csv", index=False)

print("\nSaved: evaluation/final_comparison.csv")

# ============================================================
# PLOT DETECTION RATE COMPARISON
# ============================================================

plt.figure()

plt.bar(["Classical", "Quantum"],
        [classical_detection, quantum_success])

plt.title("Detection Rate Comparison")
plt.ylabel("Detection / Success Rate")

plt.tight_layout()
plt.savefig("evaluation/final_detection_comparison.png")
plt.close()

print("Saved: evaluation/final_detection_comparison.png")

# ============================================================
# PLOT EXECUTION TIME COMPARISON
# ============================================================

plt.figure()

plt.bar(["Classical"],
        [classical_time])

plt.title("Classical Execution Time (seconds)")
plt.ylabel("Time (sec)")

plt.tight_layout()
plt.savefig("evaluation/classical_time.png")
plt.close()

print("Saved: evaluation/classical_time.png")

print("\nEvaluation comparison completed successfully.\n")