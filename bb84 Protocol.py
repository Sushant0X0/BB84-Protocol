from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.result import marginal_counts
import numpy as np
import matplotlib.pyplot as plt
import random

QiskitRuntimeService.save_account(channel="ibm_quantum", token="0281cfc4a48df38cefb1dca8b116d692f8cf474b4899a4ec84c1c20007f165a56550410cbf0015b47cb06e6367d7bfa248828ac8fca10421fdcffc381ad82e39", overwrite=True)
service = QiskitRuntimeService()
print(service.backends(simulator=False, operational=True))

def random_list(n):
    return np.random.randint(0, 2, n).tolist()

def bb84_simulator(n_bit, eve_present=False, service=None, backend_name="ibm_brisbane"):
    """
    Simulate BB84 Quantum Key Distribution protocol on an IBM QPU with readout mitigation.
    
    Args:
        n_bit (int): Number of qubits to send.
        eve_present (bool): Whether an eavesdropper (Eve) is present.
        service (QiskitRuntimeService): IBM Quantum Runtime service instance.
        backend_name (str): Name of the IBM QPU (e.g., 'ibm_brisbane').
    
    Returns:
        tuple: (Bob's sifted key, Alice's sifted key, QBER)
    """
    alice_bit = random_list(n_bit)
    alice_bases = random_list(n_bit)
    bob_bases = random_list(n_bit)
    eve_bases = random_list(n_bit) if eve_present else None
    bob_results = []

    # Get backend and prepare transpiler
    backend = service.backend(backend_name)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=3)

    # Batch circuits
    eve_circuit = []
    bob_circuit = []
    for i in range(n_bit):
        qr = QuantumRegister(1, 'q')
        cr = ClassicalRegister(1, 'c0')
        qc = QuantumCircuit(qr, cr)

        # Alice prepares qubit
        if alice_bit[i] == 1:
            qc.x(0)
        if alice_bases[i] == 1:
            qc.h(0)

        if eve_present:
            eve_qc = qc.copy()
            if eve_bases[i] == 1:
                eve_qc.h(0)
            eve_qc.measure(0, cr)
            eve_circuit.append(pm.run(eve_qc))
        else:
            eve_circuit.append(None)

        qc = QuantumCircuit(qr, cr)
        bob_circuit.append(qc)

    # Run Eve's circuits (if present)
    eve_bits = [0] * n_bit
    if eve_present:
        sampler = Sampler(mode=backend)
        job = sampler.run(eve_circuit, shots=1)
        for i, result in enumerate(job.result()):
            counts = result.data.c0.get_counts()
            eve_bits[i] = int(list(counts.keys())[0])

    # Build and run Bob's circuits
    for i in range(n_bit):
        qc = bob_circuit[i]
        if eve_present:
            if eve_bits[i] == 1:
                qc.x(0)
            if eve_bases[i] == 1:
                qc.h(0)
        else:
            if alice_bit[i] == 1:
                qc.x(0)
            if alice_bases[i] == 1:
                qc.h(0)
        if bob_bases[i] == 1:
            qc.h(0)
        qc.measure(0, cr)
        bob_circuit[i] = pm.run(qc)

    sampler = Sampler(mode=backend)
    job = sampler.run(bob_circuit, shots=1)
    for i, result in enumerate(job.result()):
        counts = result.data.c0.get_counts()
        measured_bit = int(list(counts.keys())[0])
        bob_results.append(measured_bit)

    # Sift keys
    sifted_key_alice = []
    sifted_key_bob = []
    for i in range(n_bit):
        if alice_bases[i] == bob_bases[i]:
            sifted_key_alice.append(alice_bit[i])
            sifted_key_bob.append(bob_results[i])

    # Calculate QBER
    qber = 0
    if sifted_key_alice:
        errors = sum(a != b for a, b in zip(sifted_key_alice, sifted_key_bob))
        qber = errors / len(sifted_key_alice)

    # Debugging
    print("Alice bits:", alice_bit)
    print("Bob results:", bob_results)
    print("Sifted Alice:", sifted_key_alice)
    print("Sifted Bob:", sifted_key_bob)
    print("Errors:", errors, "Sifted length:", len(sifted_key_alice))

    return sifted_key_bob, sifted_key_alice, qber

def average_of_list(list_name):
    final_sum = 0
    for i in list_name:
        final_sum += i
    avg_list = final_sum / len(list_name) if list_name else 0
    return avg_list

def main():
    """Run BB84 simulation on IBM QPU and visualize results."""
    service = QiskitRuntimeService(channel="ibm_quantum")
    
    n_bit = 20
    trial = 5
    qber_no_eve = []
    qber_with_eve = []
    
    for _ in range(trial):
        _, _, qber = bb84_simulator(n_bit, eve_present=False, service=service)
        qber_no_eve.append(qber)
        _, _, qber = bb84_simulator(n_bit, eve_present=True, service=service)
        qber_with_eve.append(qber)
    
    avg_qber_no_eve = average_of_list(qber_no_eve)
    avg_qber_with_eve = average_of_list(qber_with_eve)
    
    print("avg qber without eve ", avg_qber_no_eve)
    print("avg qber with eve ", avg_qber_with_eve)
    
    # Visualize results
    plt.figure(figsize=(8, 6))
    plt.bar(['No Eavesdropping', 'With Eavesdropping'], 
            [avg_qber_no_eve, avg_qber_with_eve], 
            color=['blue', 'red'])
    plt.ylabel('Quantum Bit Error Rate (QBER)')
    plt.title('BB84 QKD on IBM QPU: QBER Comparison')
    plt.ylim(0, 0.5)
    plt.savefig('bb84_qber_qpu_plot.png')
    plt.show()

if __name__ == "__main__":
    main()