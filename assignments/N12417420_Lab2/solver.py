#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module provides an interface for the following modes:
- A generic DPLL solver using the 'dpll' mode
- A BNF to CNF converter using the 'cnf' mode
- A direct BNF solver using the 'solver' mode.
"""

import argparse
import enum
import logging
import sys

import converter
from dpll import DPLL

class Modes(enum.Enum):
  """Enum modes to run the program"""
  cnf = 1
  dpll = 2
  solver = 3

def create_parser():
  """Creates the argument parser to control the program executions.

  Returns: An instance of `argparse.ArgumentParser`.
  """
  parser = argparse.ArgumentParser(
    description="Propositional logic solver",
    epilog="Solve it!"
  )
  parser.version = "1.0.0"
  parser.add_argument('-v', action='count', help="Enable verbosity for program runs")
  parser.add_argument('-mode', action='store', help="Mode to run the program. "
                                                    "One of cnf, dpll, solver.")
  parser.add_argument('input_file', action='store', help="Path to the input file")
  return parser

def validate_args(args):
  """Validate the arguments provided to the program

  Args:
    args: Parsed args from `argparse.ArgumentParser`.
  """
  if not args.mode:
    logging.error("please provide the -mode option (one of cnf, dpll, solver)")
    sys.exit()
  valid_modes = [mode.name for mode in Modes]
  if args.mode and args.mode not in valid_modes:
    logging.error("-mode option should be one of: cnf, dpll, solver")
    sys.exit()

def _cnf_mode(lines):
  """Helper function to run in 'cnf' mode"""
  return converter.run(lines)

def _dpll_mode(lines):
  """Helper function to run in 'dpll' mode"""
  dpll_solver = DPLL(lines)
  result = dpll_solver.run()
  if result == "NO VALID ASSIGNMENT":
    print(result)
  else:
    logging.debug("OUTPUT: ")
    for k, v in result.items():
      print(f"{k}={v}")

def solve(mode, input_file):
  """driver function for all the three modes.

  Args:
    mode: One of 'cnf', 'dpll', 'solver'
    input_file: Path to file containing sentences.
  """
  lines = []
  with open(input_file, "r") as f:
    lines = f.readlines()
  lines = [line.strip() for line in lines if line.strip()!=""]

  if mode == Modes.cnf.name:
    sentences = _cnf_mode(lines)
    for sentence in sentences:
      print(sentence)
  elif mode == Modes.dpll.name:
    _dpll_mode(lines)
  elif mode == Modes.solver.name:
    _dpll_mode(_cnf_mode(lines))

def set_logging(v):
  """Create a logger for the program

  Args:
    v: The verbosity option for the program execution
  """
  if v:
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
  else:
    logging.basicConfig(level=logging.ERROR, format='%(message)s')

if __name__ == "__main__":

  solver_parser = create_parser()
  args = solver_parser.parse_args()
  set_logging(v=args.v)
  validate_args(args=args)
  solve(args.mode, args.input_file)