import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import os

df = pd.read_csv("data/ai_detected_logs.csv")

sizes = [128, 256, 512, 1024, 2048, len(df)]
times = []

for size in sizes:
    subset = df.head(size)

    start = time.time()

    if "anomaly_score" in subset.columns:
        scores = subset["anomaly_score"].values
        max_score = scores[0]
        for i in range(1, len(scores)):
            if scores[i] > max_score:
                max_score = scores[i]

    end = time.time()
    times.append(end - start)

os.makedirs("evaluation", exist_ok=True)

result_df = pd.DataFrame({
    "dataset_size": sizes,
    "execution_time": times
})

result_df.to_csv("evaluation/classical_scalability.csv", index=False)

plt.figure()
plt.plot(sizes, times, marker="o")
plt.title("Classical Search Scalability")
plt.xlabel("Dataset Size")
plt.ylabel("Execution Time (seconds)")
plt.tight_layout()
plt.savefig("evaluation/classical_scalability.png")
plt.close()

print("Saved: evaluation/classical_scalability.csv")
print("Saved: evaluation/classical_scalability.png")