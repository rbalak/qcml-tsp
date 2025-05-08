import warnings
warnings.filterwarnings("ignore")

from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import numpy as np

# Define Oracle V1 (part of Uj)
def build_V1_oracle(theta_0, theta_1, theta_2):
    qctrl = QuantumRegister(1, 'qctrl')
    ci = QuantumRegister(2, 'ci')
    V1 = QuantumCircuit(ci ,qctrl, name="V1")
    
    V1.cp(theta_2 - theta_0, qctrl[0], ci[1])  # Controlled Phase
    V1.p(theta_0, qctrl[0])  # Phase gate
    V1.cp(theta_1 - theta_0, qctrl[0], ci[0])  # Controlled Phase
    
    return V1

# Define Oracle V2 (part of Uj)
def build_V2_oracle(theta_0, theta_1, theta_2, theta_3):
    qctrl = QuantumRegister(1, 'qctrl')
    ci = QuantumRegister(2, 'ci')
    V2 = QuantumCircuit(ci, qctrl, name="V2")

    x = -(theta_3 - theta_2 - theta_1 + theta_0) / 2

    V2.x(ci[0])  # Apply X on ci[0]
    V2.x(ci[1])  # Apply X on ci[1]
    V2.ccx(qctrl[0], ci[1], ci[0])  # Toffoli (CCX) gate
    V2.cp(x, qctrl[0], ci[0])  # Controlled Phase
    V2.ccx(qctrl[0], ci[1], ci[0])  # Toffoli gate
    V2.cp(x, qctrl[0], ci[1])  # Controlled Phase
    V2.cp(x, qctrl[0], ci[0])  # Controlled Phase
    V2.p(-2 * x, qctrl[0])  # Phase gate
    V2.x(ci[0])  # Apply X on ci[0]
    V2.x(ci[1])  # Apply X on ci[1]
    
    return V2

# Define the final Uj oracle by combining V1 and V2
def build_Uj_oracle(theta_0, theta_1, theta_2, theta_3, label, draw_circuit=False):
    V1 = build_V1_oracle(theta_0, theta_1, theta_2)
    V2 = build_V2_oracle(theta_0, theta_1, theta_2, theta_3)
    if draw_circuit:
        display(V1.draw('mpl'))  # Display V1
        display(V2.draw('mpl'))  # Display V2
    qctrl = QuantumRegister(1, 'qctrl')
    ci = QuantumRegister(2, 'ci')
    Uj = QuantumCircuit(ci, qctrl, name=label)
    # Apply both oracles in sequence
    Uj.append(V1, [0, 1, 2])  # V1 affects qctrl, ci[0], ci[1]
    Uj.append(V2, [0, 1, 2])  # V2 affects qctrl, ci[0], ci[1]
    Uj.label = label
    #display(Uj.draw('mpl'))  # Display Uj
    
    return Uj
