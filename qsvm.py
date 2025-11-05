import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler

from qiskit.circuit.library import ZZFeatureMap
from qiskit.primitives import Sampler

from qiskit_machine_learning.state_fidelities import ComputeUncompute
from qiskit_machine_learning.kernels import FidelityQuantumKernel

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from qiskit_machine_learning.algorithms import QSVC
# Load Excel file
df = pd.read_csv("mlb_game_data_2025.csv")

# Explore the structure
print(df.shape)
print(df.head(5))

# creates x for features and y for labels
X = df.drop(columns=['Home Team', 'Away Team', 'Date' ,'Home Team Won']).to_numpy()
X = StandardScaler().fit_transform(X)

Y = df['Home Team Won'].to_numpy()
df_sample = df.sample(100, random_state=42)


X = StandardScaler().fit_transform(df_sample.drop(columns=['Home Team', 'Away Team', 'Date' ,'Home Team Won']).to_numpy())
Y = df_sample['Home Team Won'].to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

feature_map = ZZFeatureMap(feature_dimension=len(X[0]), reps=2, entanglement='linear')

sampler = Sampler()

fidelity = ComputeUncompute(sampler=sampler)

kernel = FidelityQuantumKernel(fidelity=fidelity, feature_map=feature_map)

print("Starting QSVC training...")
start_time=time.time()

qsvc = QSVC(quantum_kernel=kernel)

qsvc.fit(X_train, y_train)

end_time=time.time()
qsvc_score = qsvc.score(X_test, y_test)

end_time2=time.time()

print(f"Training time: {end_time - start_time} seconds")
print(f"Scoring time: {end_time2 - end_time} seconds")
print(f"QSVC accuracy: {qsvc_score}")