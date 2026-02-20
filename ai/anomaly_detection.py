import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

print("Loading suspicious logs...")

df = pd.read_csv("data/suspicious_logs.csv")

print("Total suspicious logs:", len(df))

# Encode categorical columns
encoders = {}

for column in df.columns:
    if df[column].dtype == object:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        encoders[column] = le

# Save feature set separately
X = df.copy()

print("Training anomaly detection model...")

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(X)

# Predict using SAME feature set
anomaly_scores = model.decision_function(X)
anomaly_labels = model.predict(X)

# Convert format
anomaly_labels = np.where(anomaly_labels == -1, 1, 0)

# Add results to dataframe
df['anomaly_score'] = anomaly_scores
df['anomaly'] = anomaly_labels

# Save output
output_path = "data/ai_detected_logs.csv"
df.to_csv(output_path, index=False)

print("AI anomaly detection complete")
print("Anomalies detected:", df['anomaly'].sum())
print("Saved to:", output_path)
