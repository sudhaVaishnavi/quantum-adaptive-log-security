**Quantum-Enhanced Adaptive Secure Log Analysis System**

**Overview:**

This project implements a fully automated hybrid cybersecurity pipeline integrating big data processing, AI anomaly detection, quantum search revalidation, quantum key distribution simulation, and adaptive encryption.

The system demonstrates how quantum algorithms can be meaningfully integrated into a structured security architecture rather than used as isolated demonstrations.

**Problem Statement:**

Modern security systems detect anomalies and encrypt data, but detection intelligence and encryption policy are typically independent.

This project explores an adaptive architecture where:

→ AI detects anomalies
→ Grover’s quantum search revalidates suspicious records
→ Quantum-derived metrics influence threat classification
→ MDI-QKD simulation determines secure key quality
→ Encryption strength adapts dynamically

**System Architecture**

→ Big Data Processing
→ AI Anomaly Detection
→ Grover Quantum Revalidation
→ Threat-Level Classification
→ MDI-QKD Secure Key Simulation
→ Adaptive AES-256 Encryption

All stages are executed using an automated pipeline runner.

**Technologies Used**

→ Python
→ Apache Spark
→ Scikit-learn (Isolation Forest)
→ Qiskit (Grover simulation)
→ Qiskit Aer (noise modeling)
→ PyCryptodome (AES encryption)
→ Matplotlib (evaluation plots)

**Key Features**

→ Large-scale log simulation and filtering
→ AI-based anomaly detection
→ Grover search over anomaly indices
→ Noise-aware MDI-QKD simulation
→ QBER and secure key rate evaluation
→ Adaptive encryption based on quantum threat level
→ Classical vs quantum performance comparison
→ Automated end-to-end execution

**How to Run**
1. conda activate quantumlog
2. cd quantum-secure-log-analysis
3. python run_pipeline.py
   
**Output Artifacts**

→ Suspicious and anomaly log datasets
→ Grover success metrics and circuit depth
→ QKD QBER and secure key rate plots
→ Classical vs quantum evaluation comparison
→ Encrypted anomaly logs
→ Stage execution timing summary

**Project Scope**
This project is a research-grade simulation and does not claim real quantum advantage. It focuses on architectural integration, security modeling, and hybrid classical-quantum system design.
