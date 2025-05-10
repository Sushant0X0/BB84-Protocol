# BB84 Quantum Key Distribution Simulation

This project implements the BB84 Quantum Key Distribution (QKD) protocol using Qiskit and IBM Quantum's `ibm_brisbane` QPU. It simulates secure key exchange between Alice and Bob, with and without an eavesdropper (Eve), and compares Quantum Bit Error Rates (QBER).

## Features
- Simulates BB84 protocol with `n_bit=20` qubits over 5 trials.
- Uses Qiskit and `qiskit-ibm-runtime` for QPU execution.
- Plots QBER comparison (with/without Eve).
- Expected QBER: ~0.10–0.20 (no Eve), ~0.30–0.40 (with Eve).

## Prerequisites
- Python 3.8+
- IBM Quantum account and API token ([sign up](https://quantum-computing.ibm.com/))
- Install dependencies:
  ```bash
  pip install -r requirements.txt
