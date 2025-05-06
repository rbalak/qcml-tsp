import warnings
warnings.filterwarnings("ignore")

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import Aer
from qiskit.circuit.library import QFT, IntegerComparator
from qiskit.quantum_info import Statevector
from U_Power import build_U_power_oracle 
import numpy as np
from numpy import pi

def create_clc_oracle(theta_matrix, t, threshold):
    """
    Creates a CLC (Controlled Local Cost) gate for use in QPE-based TSP estimation.

    Parameters:
    - theta_matrix: Cost matrix (4x4)
    - t: Number of precision qubits
    - threshold: Threshold value (integer in [0, 2^t - 1])
    
    Returns:
    - QuantumCircuit: A circuit that applies QPE + Comparator logic
    """
    # Quantum Registers
    precision = QuantumRegister(t, 't')                # Precision qubits for QPE
    flag = QuantumRegister(1, 'flag')                  # Flag for marking solutions
    ancillary = QuantumRegister(t-1, 'ancillary')        # Ancilla for IntegerComparator (needs t-1 ancilla, flag is used as one of the inputs to integer comparator)
    cycle = QuantumRegister(8, 'C')                    # Cycle/tour register
    
    circuit = QuantumCircuit(precision, flag, ancillary, cycle, name="CLC")

    # Step 1: Apply superpositions
    circuit.h(precision)

    # Step 2: Apply controlled-U^2^k gates
    for k in range(t):
        U_power = build_U_power_oracle(theta_matrix, 2 ** k)
        circuit.append(U_power, [*cycle, precision[k]])

    # Step 3: Apply inverse QFT
    iqft = QFT(t, inverse=True, do_swaps=True).to_gate(label="QFT†")
    circuit.append(iqft, precision)

    # Step 4: Apply threshold comparator
    cmp_gate = IntegerComparator(num_state_qubits=t, value=threshold, geq=False, name='Cth')
    circuit.append(cmp_gate, [*precision, *flag, *ancillary])
    print("CLC Circuit")
    print("------------------------------------------------------------------------------------------------------------------------")
    display(circuit.draw('mpl'))

    return circuit
