import os
import time
import pandas as pd
import numpy as np

print("\nLoading AI detected anomalies...\n")

df = pd.read_csv("data/ai_detected_logs.csv")

total_records = len(df)

print("Total anomaly records:", total_records)

if total_records == 0:
    print("No data found.")
    exit()

# ============================================================
# CLASSICAL LINEAR SEARCH
# ============================================================

start_time = time.time()

# If anomaly_score exists, use it
if "anomaly_score" in df.columns:
    scores = df["anomaly_score"].values
    
    max_index = 0
    max_score = scores[0]

    for i in range(1, len(scores)):
        if scores[i] > max_score:
            max_score = scores[i]
            max_index = i

    detected_indices = np.where(scores > np.percentile(scores, 90))[0]

else:
    # fallback if anomaly_score column missing
    max_index = 0
    max_score = 1
    detected_indices = [0]

end_time = time.time()

execution_time = end_time - start_time

detected_attacks = len(detected_indices)

detection_rate = detected_attacks / total_records

print("\nClassical Search Results:")
print("Highest anomaly index:", max_index)
print("Detected attacks:", detected_attacks)
print("Execution time (seconds):", execution_time)
print("Detection rate:", detection_rate)

# ============================================================
# SAVE RESULTS
# ============================================================

os.makedirs("evaluation", exist_ok=True)

results = {
    "total_records": total_records,
    "detected_attacks": detected_attacks,
    "detection_rate": detection_rate,
    "execution_time_seconds": execution_time
}

df_out = pd.DataFrame([results])

df_out.to_csv("evaluation/classical_results.csv", index=False)

print("\nSaved: evaluation/classical_results.csv\n")