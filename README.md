# Quantum Machine Learning for MLB Game Prediction

**Course:** ECE 733 – Quantum Machine Learning, University of Waterloo
**Authors:** Jonathan & Danesh Morales
**GitHub:** [DaneshMorales/QML_project](https://github.com/DaneshMorales/QML_project)

---

## Overview

This project applies quantum and classical machine learning to predict the outcomes of MLB (Major League Baseball) playoff games. We trained and evaluated four families of classifiers — Variational Quantum Circuits (VQC), Quantum Support Vector Machines (QSVM), classical SVMs, and MLP neural networks — on a feature-engineered dataset built from the full 2025 MLB regular season.

The core goal was to benchmark quantum ML methods against classical baselines on a real-world binary classification problem and assess their practical viability.

---

## Methods & Pipeline

### 1. Data Collection
- Extracted post-game statistics for all **2,430 games** of the 2025 MLB regular season using the `mlbstatsapi` library (MLB Stats API)
- Collected playoff game data for **47 post-season games** as the held-out test set

### 2. Feature Engineering
- Computed **40-game rolling averages** for each team to capture recent form while avoiding look-ahead bias (each game's features use only prior games)
- Filtered to games where both teams had played at least 10 prior games → **2,084 training samples**
- Constructed 9 features as **home minus away differences** in key statistics:

| # | Feature |
|---|---------|
| 1 | Hits |
| 2 | Home Runs |
| 3 | Left on Base |
| 4 | On-Base Percentage (OBP) |
| 5 | Slugging Percentage (SLG) |
| 6 | Strikeouts |
| 7 | Strike Percentage |
| 8 | WHIP (Walks + Hits per Inning Pitched) |
| 9 | Starting Pitcher ERA |

- **Target:** Binary — 1 if home team wins, 0 if away team wins

### 3. Preprocessing
- Standardized all features (zero mean, unit variance)
- Mapped to angle encoding for quantum circuits: `φ = π × tanh(z)` for stable range `(-π, π)`

### 4. Models Trained

#### Variational Quantum Circuits (VQC) — 48 configurations
Built with Qiskit. Systematically swept over:
- **Feature maps:** Z, ZZ — with 1 or 2 repetitions
- **Ansätze:** RealAmplitudes, TwoLocal (RY/RZ + CX), EfficientSU2 — with 1 or 2 repetitions
- **Optimizers:** COBYLA (300 iterations), SPSA (500 iterations)
- 9 qubits (one per feature)

#### Quantum SVM (QSVM) — 4 configurations
- Quantum kernel via `FidelityQuantumKernel` (state fidelity between feature-mapped states)
- Feature maps: ZZFeatureMap, Pauli (Z, Y, ZZ) — with 1 or 2 repetitions
- Classifier: `QSVC` (Quantum Support Vector Classifier)

#### Classical SVM — 4 kernels
- Scikit-learn `SVC` with linear, polynomial, RBF, and sigmoid kernels

#### MLP Classifier — 10 configurations
- Scikit-learn `MLPClassifier`, testing solvers (Adam, SGD, LBFGS) and hidden layer configurations

---

## Results

All models tested on **47 MLB playoff games** (held-out test set).

| Model | Best Configuration | Accuracy |
|-------|--------------------|----------|
| Classical SVM | RBF kernel | **68.09%** (32/47) |
| VQC | Z-FM (2 reps) + TwoLocal (1 rep) + SPSA | **65.96%** (31/47) |
| MLP Classifier | Adam + (3,) hidden layer + α=0.001 | **61.70%** (29/47) |
| Classical SVM | Linear kernel | 55.32% (26/47) |
| Classical SVM | Polynomial kernel | 55.32% (26/47) |

**Key findings:**
- All models exceeded the 50% random baseline, confirming the rolling-average features carry genuine predictive signal
- The best VQC (65.96%) was competitive with the best classical SVM (68.09%), demonstrating quantum methods can approach classical performance on real tabular data
- Among the 48 VQCs, accuracy ranged from 31.9% to 66.0%, showing strong sensitivity to feature map and ansatz choices
- Classical SVM training: ~0.15 seconds; QSVM training: ~33–50 seconds — a significant computational trade-off at current noise levels
- Simpler MLP architectures (3 hidden neurons) outperformed deeper ones, suggesting the task does not benefit from additional model complexity

---

## Technologies

- **Python**, Jupyter Notebooks
- **Qiskit** & **Qiskit Machine Learning** — VQC, QSVM, quantum kernels, feature maps, ansätze, optimizers
- **scikit-learn** — SVM, MLPClassifier, preprocessing
- **mlbstatsapi** — MLB Stats API wrapper for data extraction
- **pandas**, **NumPy** — data processing and feature engineering

---

## Repository Structure

```
QML_project/
├── functions.py                    # MLB API helper functions
├── Datasets/
│   ├── mlb_vqc_features.csv        # Final training dataset (2084 samples, 9 features)
│   ├── postseason_test_processed.csv  # Test set (47 playoff games)
│   └── ...                         # Intermediate datasets
├── VQC_Results/                    # Predictions from all 48 VQCs
├── QSVM_Results/                   # Predictions from all 4 QSVMs
├── SVM_Results/                    # Predictions from all 4 classical SVMs
├── MLPC_Results/                   # Predictions from all 10 MLP configs
├── vqc_final.ipynb                 # Train all 48 VQCs
├── qsvm_final.ipynb                # Train all 4 QSVMs
├── svm_final.ipynb                 # Train all 4 classical SVMs
├── mlpc_final.ipynb                # Train all 10 MLP classifiers
├── vqc_table.ipynb                 # Summarize and rank VQC results
├── rolling_average.ipynb           # Build rolling-average dataset
└── extract_data.ipynb              # MLB API data extraction
```

To reproduce results, run each `*_final.ipynb` notebook end-to-end. Predictions are saved to the corresponding results folders. Run `vqc_table.ipynb` to generate the VQC accuracy ranking table.
