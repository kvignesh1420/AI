#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module provides an interface for the
K Means classifier
"""

import argparse
import logging
import sys
from learning import KMeans
from common import e2_distance
from common import manh_distance

def create_parser():
  """Creates the argument parser to control the program executions.

  Returns:
    An instance of `argparse.ArgumentParser`.
  """
  parser = argparse.ArgumentParser(
    description="K Means Classifier",
    epilog="Choose the best centroid!"
  )
  parser.version = "1.0.0"
  parser.add_argument('-v', action='count', help="Enable verbosity for program runs")
  parser.add_argument('-d', type=str, action='store', default="e2", help="distance "
                        "function to determine the closeness of points. Should be one of "
                        "'e2': euclidean squared, 'manh': manhattan. Defaults to 'e2'.")
  parser.add_argument('-data', type=str, required=True, action='store',
                                help="A file containing the data to cluster.")
  parser.add_argument('centroids', nargs='+', type=str, action='store',
                                help="Initial centroids for clustering.")
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
  k_means = KMeans(
    dist_function=dist_function,
    data_file=args.data,
    centroids=args.centroids
  )
  k_means.run()

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
