#!/usr/bin/env python3

# Author: J. Daniel Escánez
# Ingeniería Informática - Universidad de La Laguna
# Trabajo Fin de Grado: QuantumSolver

## E91 Simulator Main Program

import signal
import sys
from e91.e91 import E91

def signal_handler(sig, frame):
  print('\n\n[$] Exiting successfully\n')
  sys.exit()

if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)
  token = sys.argv[1] if len(sys.argv) > 1 else None
  e91 = E91(token)
  e91.run()
