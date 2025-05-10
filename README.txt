BB84 Quantum Key Distribution Simulation

This project implements the BB84 Quantum Key Distribution (QKD) protocol using Qiskit and IBM Quantum's ibm_brisbane QPU. It simulates secure key exchange between Alice and Bob, with and without an eavesdropper (Eve), and compares Quantum Bit Error Rates (QBER).

Project Overview





Objective: Simulate BB84 QKD to generate shared keys and measure QBER.



Setup: Uses n_bit=20 qubits over 5 trials on ibm_brisbane.



Features:





Simulates Alice’s preparation, Bob’s measurement, and Eve’s intercept-resend attack.



Outputs QBER: ~0.10–0.20 (no Eve), ~0.30–0.40 (with Eve).



Generates a QBER comparison plot 





Output:





Console: QBER values, Alice/Bob bits, sifted keys.

Challenges and Errors





High QBER (~0.54–0.56):





Causes:





Incorrect sifted key construction (appending lists instead of bits).



Single circuit accumulation, corrupting qubit states.



Flawed Eve’s logic (re-preparation after measurement).



Incorrect QBER calculation (nested loops with premature breaks).



Rectifications:





Fixed sifting to append individual bits.



Used fresh circuits per qubit to prevent gate accumulation.



Corrected Eve’s intercept-resend logic with separate circuits.



Implemented accurate QBER calculation using zip.

Code Optimization





Batching Circuits:





Reduced from 200 individual jobs to ~10–20 by batching Eve’s and Bob’s circuits.



Efficient Debugging:





Added prints for sifted keys and errors to verify correctness.

Runtime





Original: ~100 hours (free-tier) or ~17 hours (premium) for 200 circuits (no batching).



Optimized: ~5 hours (free-tier) or ~1 hour (premium) with batching.



Simulator: ~1–2 minutes using FakeBrisbane for testing.

License

MIT License
