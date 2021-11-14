#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module provides an interface for the markov process solver
"""

import argparse
import logging
import re
import sys
from yacc_parser import lexer, parser
from common import Graph
from solver import MarkovProcessSolver

def create_parser():
  """Creates the argument parser to control the program executions.

  Returns:
    An instance of `argparse.ArgumentParser`.
  """
  parser = argparse.ArgumentParser(
    description="Markov process solver",
    epilog="Approximate the best approach!"
  )
  parser.version = "1.0.0"
  parser.add_argument('-v', action='count', help="Enable verbosity for program runs")
  parser.add_argument('-df', type=float, action='store', default=1.0,
                      help="future reward discount factor in the range [0, 1]. Defaults to 1.0")
  parser.add_argument('-min', type=bool, action='store', default=False, help="minimize "
                        "values as costs, defaults to False which maximizes values as rewards")
  parser.add_argument('-tol', type=float, action='store', default=0.01, help="tolerance for "
                                                    "each value iteration. Defaults to 0.01")
  parser.add_argument('-iter', type=int, action='store', default=100, help="Maximum number of "
                                  "value iteration updates before termination. Defaults to 100")
  parser.add_argument('input_file', action='store', help="Path to the input file")
  return parser

def validate_args(args):
  """Validate the arguments provided to the program

  Args:
    args: Parsed args from `argparse.ArgumentParser`.
  """
  if args.df < 0 or args.df > 1:
    sys.exit(f"Discount factor df = {args.df} is not in the range of [0, 1]")
  if args.iter < 0:
    sys.exit("cutoff for value interations should be non-negative, "
                              f"but got option -iter = {args.iter}")

def handle_unseparated_floats(line):
  """Handle lines with probabilities which are not-separated by
  whitespace.
  """
  if "%" in line:
    pattern = r'\.[0-9]+(e[-+]?[0-9]+)?\.[0-9]+(e[-+]?[0-9]+)?'
    if re.search(pattern, line) is not None:
      sys.exit(f"Invalid probabilities in line: {line}")

def format_input_file(input_file):
  """Validate the contents of the input file.

  The function aims to validate the input file by performing sanity
  checks based on node and edge creation.

  Args:
    input_file: Path to the input file which describes the markov process.

  Returns:
    Formatted lines of the file.
  """
  input_file = args.input_file
  lines = []
  with open(input_file, "r") as f:
    lines = f.readlines()
  fmt_lines = []
  for line in lines:
    if line.startswith("#"):
      continue
    fmt_line = line.replace("\n", "").strip()
    if fmt_line:
      handle_unseparated_floats(fmt_line)
      fmt_line = parser.parse(fmt_line)
      fmt_lines.append(fmt_line)
  return fmt_lines

def assign_values(g, all_tokens):
  """Add nodes to graph and assign values to them

  Args:
    g: An instance of `common.Graph`
    all_tokens: tokens of all lines parsed by lex

  Returns:
    An instance of `common.Graph` with added nodes.
  """
  for tokens in all_tokens:
    if tokens[1].type == "EQUALS":
      g.add_node(name=tokens[0].value, value=float(tokens[2].value))
  return g

def assign_probabilities(g, all_tokens):
  """Assign probabilities to the graph nodes

  Args:
    g: An instance of `common.Graph`
    all_tokens: tokens of all lines parsed by lex

  Returns:
    An instance of `common.Graph` with updated/added nodes.
  """
  for tokens in all_tokens:
    if tokens[1].type == "MOD":
      node_name = tokens[0].value
      probs = []
      for token in tokens[2:]:
        probs.append(float(token.value))
      if node_name not in g.nodes:
        g.add_node(name=node_name)
      g.nodes[node_name].probs = probs
  return g

def assign_edges(g, all_tokens):
  """Add edges to nodes in the graph

  Args:
    g: An instance of `common.Graph`
    all_tokens: tokens of all lines parsed by lex

  Returns:
    An instance of `common.Graph` with added edges.
  """
  for tokens in all_tokens:
    if tokens[1].type == "COLON":
      parent_node_name = tokens[0].value
      if parent_node_name not in g.nodes:
        g.add_node(name=parent_node_name)
      for token in tokens[2:]:
        if token.type == "ATOM":
          node_name = token.value
          if node_name not in g.nodes:
            g.add_node(name=node_name)
          g.add_edge(parent_node_name, node_name)
  return g

def validate_nodes(g):
  """Validate nodes based on the following rules:

  - If a node has edges but no probability entry,
    it is assumed to be a decision node with p=1
  - If a node has edges but no reward entry, it is
    assumed to have a reward of 0
  - If a node has no edges it is terminal. A probability
    entry for such a node is an error.

  Args:
    g: An instance of `common.Graph`

  Returns:
    An instance of `common.Graph` with validated nodes.
  """
  node_names = g.nodes
  for node_name in node_names:
    node = g.nodes[node_name]
    if g.edges[node_name] == [] and node.probs is not None:
      sys.exit(f"Node {node_name} has no edges but has a probability entry")
    if g.edges[node_name] != [] and node.probs is None:
      node.probs = [1]
    if g.edges[node_name] != [] and node.value is None:
      node.value = 0
    g.nodes[node_name] = node
  return g

def assign_node_types(g):
  """Assign types to nodes based on its values and probs
  attributes.

  Args:
    g: An instance of `common.Graph`

  Returns:
    An instance of `common.Graph` with updated nodes.
  """
  node_names = g.nodes
  for node_name in node_names:
    node = g.nodes[node_name]
    if node.probs is None:
      node.type = "TERMINAL"
    elif len(node.probs) == 1:
      if len(g.edges[node_name]) == 1:
        node.type = "CHANCE"
      else:
        node.type = "DECISION"
    elif len(node.probs) > 1:
      node.type = "CHANCE"
    g.nodes[node_name] = node
  return g

def create_graph(lines):
  """Create the graph based on the formatted lines

  Args:
    lines: A list of formatted lines

  Returns:
    A `common.Graph` instance else exits the program
  """
  g = Graph()
  all_tokens = []
  for line in lines:
    lexer.input(line)
    tokens =[token for token in lexer]
    all_tokens.append(tokens)
  g = assign_values(g=g, all_tokens=all_tokens)
  g = assign_probabilities(g=g, all_tokens=all_tokens)
  g = assign_edges(g=g, all_tokens=all_tokens)
  g = validate_nodes(g=g)
  g = assign_node_types(g=g)
  return g

def solve(args):
  """Solve the markov process defined as per the content in input_file.

  Args:
    args: parsed and validated args from `argparse.ArgumentParser`.
  """
  lines = format_input_file(input_file=args.input_file)
  g = create_graph(lines=lines)
  transition_matrix = g.get_transition_matrix()
  rewards = g.get_rewards()
  mps = MarkovProcessSolver(
    g=g,
    transition_matrix=transition_matrix,
    rewards=rewards,
    df=args.df,
    max_iters=args.iter,
    tolerance=args.tol,
    minimize_cost=args.min
  )
  policy, values = mps.run()
  print_policy(policy)
  print_values(g, values)

def print_policy(policy):
  """Print policy in a readable fashion"""
  print("------------ POLICY ------------")
  for state, choice in policy.items():
    print(f"{state} -> {choice}")

def print_values(g, values):
  """Print policy in a readable fashion"""
  print("------------ VALUES ------------")
  decoding_map = g.decoding_map
  for idx, value in enumerate(values):
    print(f"{decoding_map[idx]} = {round(value,3)}")

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
