from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate

def create_state_circuit():
    qc = QuantumCircuit(9)

    # Step 1: Define target bitstrings
    marked_states = [
        '00011110',
        '00111001',
        '01001011',
        '01110010',
        '10001101',
        '10010011',
    ]

    # Step 2: For each bitstring, apply X to match 0s, MCX, then undo X
    for bitstring in marked_states:
        control_qubits = list(range(8))
        target_qubit = 8

        # Apply X to control qubits where bit is '0'
        for i, bit in enumerate(bitstring):
            if bit == '0':
                qc.x(i)

        # Apply multi-controlled X gate
        qc.mcx(control_qubits, target_qubit)

        # Undo the X gates
        for i, bit in enumerate(bitstring):
            if bit == '0':
                qc.x(i)

    return qc
