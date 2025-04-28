import warnings
warnings.filterwarnings("ignore")

from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import numpy as np
from Uj import build_Uj_oracle

def build_U_oracle(theta_matrix, draw_circuit=False):
    """
    Builds a complete U oracle for N=4 cities, using Uj oracles.
    
    Args:
        theta_matrix: 4x4 list of theta parameters for each city pair

    Returns:
        U_oracle_gate: a Gate object that can be used in a larger circuit
    """
    # --- Initialize quantum registers ---
    qctrl = QuantumRegister(1, 'qctrl')
    tour = QuantumRegister(8, 'c')  # 4 cities × 2 bits
    circuit = QuantumCircuit(tour, qctrl, name='U')

    # --- Apply Uj for each pair (city_j, city_{j+1}) ---
    N = 4
    for j in range(N):
        theta_0 = theta_matrix[j][0]
        theta_1 = theta_matrix[j][1]
        theta_2 = theta_matrix[j][2]
        theta_3 = theta_matrix[j][3]

        # Build the oracle for this city pair
        Uj_oracle = build_Uj_oracle(theta_0, theta_1, theta_2, theta_3, label=f"U{j+1}", draw_circuit=draw_circuit)

        # Append to the main circuit; Uj acts on (ci_j, ci_{j+1}, qctrl)
        # City i is encoded in 2 qubits: 2j and 2j+1
        circuit.append(Uj_oracle, [tour[2*j], tour[2*j + 1], qctrl[0]])

    return circuit


def build_U_power_oracle(theta_matrix, power, draw_circuit=False):
    """
    Builds the controlled U^power gate for use in QPE.
    
    Args:
        theta_matrix (list of list): 4x4 matrix of theta parameters.
        power (int): Exponent to which U is raised.
    
    Returns:
        U_power_gate (Gate): Gate object for U^power.
    """
    U_gate = build_U_oracle(theta_matrix, draw_circuit)

    # Repeat the U circuit 'power' times
    qctrl = QuantumRegister(1, 'qctrl')
    tour = QuantumRegister(8, 'c')
    qc_power = QuantumCircuit(tour, qctrl, name=f"U^{power}")

    for i in range(power):
        qc_power.append(U_gate, [*tour, qctrl[0]])

    return qc_power