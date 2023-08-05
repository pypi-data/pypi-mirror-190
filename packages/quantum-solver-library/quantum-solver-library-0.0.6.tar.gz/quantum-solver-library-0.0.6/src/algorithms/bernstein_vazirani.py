#!/usr/bin/env python3

# Author: J. Daniel Escánez
# Ingeniería Informática - Universidad de La Laguna
# Trabajo Fin de Grado: QuantumSolver

from qiskit import QuantumCircuit
from algorithms.qalgorithm import QAlgorithm

## Bernstein-Vazirani Algorithm Implementation for QuantumSolver
## @see https://qiskit.org/textbook/ch-algorithms/bernstein-vazirani.html
class BernsteinVazirani(QAlgorithm):
  ## Constructor
  def __init__(self):
    ## The name of the algorithm
    self.name = 'Bernstein-Vazirani'
    ## A short description
    self.description = 'Using an oracle: f(x) = (s * x) mod 2. Obtain s (a secret number)'
    ## The required parameters for the algorithm
    self.parameters = [
      {
        'type': 'string',
        'description': 'The secret binary number s, to generate the oracle',
        'constraint': 'The length must be smaller than the number of qubits of the selected backend'
      }
    ]
    ## How to parse the result of the circuit execution
    self.parse_result = lambda counts: list(counts.keys())[0]
    ## How to parse the input parameters
    self.parse_parameters = lambda parameters: [parameters[0]]
    
  ## Verify that the parameter is a binary string
  def check_parameters(self, parameters):
    if len(parameters) == 1 and type(parameters[0]) == str:
      return all([qubit == '0' or qubit == '1' for qubit in parameters[0]])
    return False

  ## Create the circuit
  def circuit(self, secret_number='01011'):
    n = len(secret_number)
    n_range = list(range(n))
    
    # Create a Quantum Circuit acting on the q register
    circuit = QuantumCircuit(n + 1, n)
    
    circuit.x(n)
    circuit.h(n_range + [n])

    circuit.barrier()

    for i, char in enumerate(reversed(secret_number)):
      if char == '1':
        circuit.cx(i, n)

    circuit.barrier()

    circuit.h(n_range)

    # Map the quantum measurement to the classical bits
    circuit.measure(n_range, n_range)

    return circuit
