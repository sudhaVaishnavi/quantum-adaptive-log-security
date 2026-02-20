import subprocess
import time
import sys
from datetime import datetime

# ============================================================
# PIPELINE CONFIGURATION
# ============================================================

STEPS = [
    ("Big Data Processing", "python bigdata/spark_processing.py"),
    ("AI Anomaly Detection", "python ai/anomaly_detection.py"),
    ("Quantum Grover Search", "python quantum/grover_search.py"),
    ("MDI-QKD Simulation", "python quantum/mdi_qkd.py"),
    ("Adaptive Quantum Encryption", "python quantum/adaptive_security_pipeline.py"),
    ("Evaluation & Comparison", "python evaluation/comparison.py")
]

# ============================================================
# EXECUTION
# ============================================================

def run_pipeline():

    print("\n" + "="*60)
    print("QUANTUM-SECURE LOG ANALYSIS PIPELINE")
    print("Started at:", datetime.now())
    print("="*60 + "\n")

    total_start = time.time()
    results_summary = []

    for step_name, command in STEPS:

        print(f"\n>>> Running Stage: {step_name}")
        print("-"*50)

        start_time = time.time()

        result = subprocess.run(command, shell=True)

        end_time = time.time()
        duration = round(end_time - start_time, 2)

        if result.returncode != 0:
            print(f"\n❌ Stage Failed: {step_name}")
            print("Pipeline aborted.\n")
            sys.exit(1)

        print(f"✅ Stage Completed: {step_name} ({duration} seconds)")
        results_summary.append((step_name, duration))

    total_end = time.time()
    total_duration = round(total_end - total_start, 2)

    print("\n" + "="*60)
    print("PIPELINE EXECUTION SUMMARY")
    print("="*60)

    for name, duration in results_summary:
        print(f"{name:<35} : {duration} sec")

    print("-"*60)
    print(f"{'Total Execution Time':<35} : {total_duration} sec")
    print("="*60)

    print("\nPipeline completed successfully.\n")

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    run_pipeline()