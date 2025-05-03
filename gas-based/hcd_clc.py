import warnings
warnings.filterwarnings("ignore")

from qiskit import QuantumCircuit, QuantumRegister
from hcd_encoding import create_state_circuit
from clc import create_clc_oracle
import numpy as np
from numpy import pi


def create_hcd_clc_oracle(theta_matrix, t, threshold):

    # --- Quantum Registers ---
    precision = QuantumRegister(t, 't')        # Phase estimation qubits
    cth_flag = QuantumRegister(1, 'cth_flag')          # Marking solutions which are under the threshold
    hamiltonian_flag = QuantumRegister(1, 'hamiltonian_flag')
    ancillary = QuantumRegister(5, 'ancillary')
    cycle = QuantumRegister(8, 'C')            # Cycle qubits`

    qc = QuantumCircuit(cycle, hamiltonian_flag, precision, cth_flag, ancillary)

    hcd = create_state_circuit()
    qc.append(hcd, [*cycle, *hamiltonian_flag])

    clc = create_clc_oracle(theta_matrix, t, threshold)
    qc.append(clc,[*precision, *cth_flag, *ancillary, *cycle])   

    return qc






