#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module provides an interface for the
K Nearest Neighbors classifier
"""

import argparse
import logging
import sys
from learning import KNearestNeighbors
from common import e2_distance
from common import manh_distance

def create_parser():
  """Creates the argument parser to control the program executions.

  Returns:
    An instance of `argparse.ArgumentParser`.
  """
  parser = argparse.ArgumentParser(
    description="K Nearest Neighbor Classifier",
    epilog="Choose the nearest K neighbors"
  )
  parser.version = "1.0.0"
  parser.add_argument('-v', action='count', help="Enable verbosity for program runs")
  parser.add_argument('-k', type=int, action='store', default=3,
                    help="Number of nearest neighbors needed to determine the class. "
                          "Defaults to 3.")
  parser.add_argument('-d', type=str, action='store', default="e2", help="distance "
                        "function to determine the closeness of neighbors. Should be one of "
                        "'e2': euclidean squared, 'manh': manhattan. Defaults to 'e2'.")
  parser.add_argument('-unitw', type=bool, action='store', default=False, help="Whether to use "
                        "unit voring weights or not. If not, we use 1/d as the voting strength of "
                        "each neighbor. Defaults to False.")
  parser.add_argument('-train', type=str, required=True, action='store',
                                help="Path to the training data file")
  parser.add_argument('-test', type=str, required=True, action='store',
                                help="Path to the testing data file")
  return parser

def validate_args(args):
  """Validate the arguments provided to the program

  Args:
    args: Parsed args from `argparse.ArgumentParser`.
  """
  if args.d not in ["e2", "manh"]:
    sys.exit(f"Distance function -d = '{args.d}' is not one of 'e2', 'manh'")

def solve(args):
  """Solve the markov process defined as per the content in input_file.

  Args:
    args: parsed and validated args from `argparse.ArgumentParser`.
  """
  dist_function = e2_distance if args.d == "e2" else manh_distance
  k_nn = KNearestNeighbors(
    k=args.k,
    dist_function=dist_function,
    unitw=args.unitw,
    train_file=args.train,
    test_file=args.test
  )
  k_nn.run()

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
  solve(args)
