#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module provides an interface to leverage:
- Breadth First Search
- Iterative Deepending and
- A*
search algorithms to find a path from start node to goal in a graph.
"""
import argparse
import enum
import logging
import sys

import search
from common import Graph
from common import is_alphanumeric


class Algorithms(enum.Enum):
  BFS = 1
  ID = 2
  ASTAR = 3

def create_parser():
  """Creates the argument parses for controlling the program runs

  Returns: An instance of `argparse.ArgumentParser`.
  """
  parser = argparse.ArgumentParser(
    description="Find a path from start node to a goal node",
    epilog="Search until you find it!"
  )
  parser.version = "1.0.0"
  parser.add_argument('-v', action='count', help="Enable verbosity for program runs")
  parser.add_argument('-start', action='store', help="Name of the start node")
  parser.add_argument('-goal', action='store', help="Name of the goal node")
  parser.add_argument('-alg', action='store', help="One of: BFS, ID, ASTAR")
  parser.add_argument('-depth', type=int, action='store', help="Initial search depth (ONLY) "
                                                     "for Iterative Deepening (ID)")
  parser.add_argument('graph_file', action='store', help="Path to the graph input")
  return parser

def validate_args(args):
  """Validate the arguments provided to the program

  Args:
    args: Parsed args from `argparse.ArgumentParser`.

  Returns:
    a validated instance of `common.Graph`
  """
  if args.start and args.goal and not args.alg:
    logging.error("please provide the -alg option (one of BFS, ID, ASTAR)")
    sys.exit()
  valid_algorithms = [algorithm.name for algorithm in Algorithms]
  if args.alg and args.alg not in valid_algorithms:
    logging.error("-alg option should be one of: BFS, ID, ASTAR")
    sys.exit()
  if args.alg and (args.start is None or args.goal is None):
      logging.error(f"Please provide a valid -start and -goal for {args.alg}")
      sys.exit()
  if args.depth is not None and args.alg != Algorithms.ID.name:
    logging.error("-depth option can be specified only for the "
                     "iterative deepening approach. Make sure to set "
                     "-alg ID when using this.")
    sys.exit()
  if args.depth is None and args.alg == Algorithms.ID.name:
    logging.error("-depth option should be specified for the "
                     "iterative deepening approach.")
    sys.exit()
  graph = validate_graph_file(args=args)
  if args.start and args.start not in graph.get_node_names():
    logging.error(f"-start {args.start} should be a valid node in the graph")
    sys.exit()
  if args.goal and args.goal not in graph.get_node_names():
    logging.error(f"-goal {args.goal} is not a valid node in the graph")
    sys.exit()
  return graph


def validate_graph_file(args):
  """Validate the contents of the input graph file.

  The function aims to validate the file by performing sanity
  checks based on node and edge creation.

  Args:
    graph_file: Path to the input file which describes the graph
      structure.

  Returns:
    a validated instance of `common.Graph`
  """
  graph_file = args.graph_file
  lines = []
  with open(graph_file, "r") as gf:
    lines = gf.readlines()

  fmt_lines = []
  for line in lines:
    if line.startswith("#"):
      continue
    fmt_line = line.replace("\n", "").strip()
    if fmt_line:
      fmt_lines.append(fmt_line)

  graph = Graph()
  node_creators = []
  edge_creators = []
  for line in fmt_lines:
    entities = line.split(" ")
    if len(entities) == 3:
      node_name = entities[0]
      if not is_alphanumeric(node_name):
        logging.error(f"Invalid node name: {node_name} encountered")
        sys.exit()
      node_creators.append(entities)
    elif len(entities) == 2:
      node_name1 = entities[0]
      node_name2 = entities[1]
      if not is_alphanumeric(node_name1) or not is_alphanumeric(node_name2):
        logging.error(f"Unable to add an edge from {node_name1} to {node_name2} "
                       "as the node name(s) are not alphanumeric")
        sys.exit()
      edge_creators.append(entities)
    else:
      logging.error(f"Invalid line in the graph file. Found: '{line}' which "
                      "is neither a comment, vertex nor an edge.")
      sys.exit()

  for item in node_creators:
    graph.add_node(name=item[0], x=item[1], y=item[2])
  for item in edge_creators:
    graph.add_edge(name1=item[0], name2=item[1])

  return graph

def find_path(graph, alg, start, goal, depth=None):
  """Find the path from start to goal in the graph using
  algorithm `alg`

  Args:
    graph: An instance of `common.Graph`
    alg: One of the `Algorithms`
    start: start node for the search
    goal: destination node for the search
    depth: depth value for iterative deepening
  """
  if alg == Algorithms.BFS.name:
    return search.bfs(graph=graph, start=start, goal=goal)
  if alg == Algorithms.ID.name:
    return search.ids(graph=graph, start=start, goal=goal, depth=depth)
  if alg == Algorithms.ASTAR.name:
    return search.astar(graph=graph, start=start, goal=goal)

def set_logging(v):
  """Create a logger for the program

  Args:
    v: The verbosity option with which the program is
      being executed.
  """
  if args.v:
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
  else:
    logging.basicConfig(level=logging.ERROR, format='%(message)s')


if __name__ == "__main__":

  path_parser = create_parser()
  args = path_parser.parse_args()
  set_logging(v=args.v)
  graph = validate_args(args=args)
  if args.start and args.goal:
    path = find_path(
      graph=graph,
      alg=args.alg,
      start=args.start,
      goal=args.goal,
      depth=args.depth
    )
    print(path)