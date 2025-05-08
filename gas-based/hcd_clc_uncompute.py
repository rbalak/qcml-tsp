import warnings
warnings.filterwarnings("ignore")

from qiskit import QuantumCircuit, QuantumRegister
import numpy as np
from numpy import pi
from hcd_clc import create_hcd_clc_oracle

def create_hcd_clc_uncompute_oracle(threshold):
    t = 6  # number of precision qubits
    # threshold = 13  # threshold in phase units (0–63 since t=6)


    theta_matrix = np.array([
        [0, pi/16, pi/32, pi/8],  # distances from city 0
        [pi/8, 0, pi/16, pi/32],  # distances from city 1
        [pi/16, pi/8, 0, pi/16],  # distances from city 2
        [pi/16, pi/32, pi/8, 0]   # distances from city 3
    ])


    # --- Quantum Registers ---
    precision = QuantumRegister(t, 't')        # Phase estimation qubits
    cth_flag = QuantumRegister(1, 'cth_flag')          # Marking solutions which are under the threshold
    hamiltonian_flag = QuantumRegister(1, 'hamiltonian_flag')
    ancillary = QuantumRegister(5, 'ancillary')
    cycle = QuantumRegister(8, 'C')            # Cycle qubits


    qc = QuantumCircuit(hamiltonian_flag,precision, cth_flag, ancillary, cycle)
    # qc.h(cycle)
    clc_hcd = create_hcd_clc_oracle(theta_matrix, t, threshold)
    qc.append(clc_hcd,[*cycle, *hamiltonian_flag, *precision, *cth_flag, *ancillary])
    qc.cz(cth_flag[0], hamiltonian_flag[0])
    qc.append(clc_hcd.inverse(),[*cycle, *hamiltonian_flag, *precision, *cth_flag, *ancillary])

    return qc
