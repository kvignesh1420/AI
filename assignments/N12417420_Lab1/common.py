#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module maintains common data structures and functions
for implementing the algorithms.
"""
import math
import logging
import re
import sys

def is_alphanumeric(token):
  """Checks if a token is alphamumeric or not:

  Args:
    token: a string to validate

  Returns:
    A boolean

  Examples:
    is_alphanumeric("abcd") -> True
    is_alphanumeric("1212") -> True
    is_alphanumeric("abc121d") -> True
    is_alphanumeric("abcd$#") -> False
    is_alphanumeric("$1dx") -> False
  """
  pattern = "^[a-zA-Z0-9]*$"
  pattern_obj = re.compile(pattern=pattern)
  if not token:
    return False
  if(re.search(pattern_obj, token)):
    return True
  return False

def euclidean_distance(node1, node2):
  """Calculate the euclidean distance between two nodes

  Args:
    node1: start node of type `Node`.
    node2: destination node of type `Node`.

  Returns: euclidean distance between the two nodes
  """
  return round(math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2), 2)

class Node():
  """A class to represent the nodes of a graph

  Args:
    name: The name of the node
    x: X co-ordinate of the node
    y: Y co-ordinate of the node
  """
  def __init__(self, name, x, y) -> None:
    self.name = name
    self.x = x
    self.y = y
    self._parse_args()

  def _parse_args(self):
    """Validate the input args"""
    try:
      self.x = int(self.x)
      self.y = int(self.y)
    except ValueError:
      logging.error(f"Non-integral co-ordinates found for node: {self.name}")
      sys.exit()

  def __str__(self) -> str:
    return self.name

  def __repr__(self) -> str:
    return self.name

  def __hash__(self) -> int:
    return hash(self.name)

class Graph():
  """A class to represent graphs along with helper functionality."""
  def __init__(self) -> None:
    self.g = {}
    self.nodes = {}

  def get_node_names(self):
    """Return a list of node names"""
    return list(self.nodes.keys())

  def add_node(self, name, x, y):
    """Add a node to the graph

    Args:
      name: The name of the node
      x: X co-ordinate of the node
      y: Y co-ordinate of the node
    """
    if name in self.get_node_names():
      logging.error(f"A node with the name {name} has already been added "
                    "to the graph.")
      sys.exit()
    node = Node(name=name, x=x, y=y)
    self.g[name] = []
    self.nodes[name] = node

  def add_edge(self, name1, name2):
    """Add an undirected edge from Node(name1,...) -- Node(name2, ...)

    Args:
      name1: Name of the first node
      name2: Name of the second node
    """
    if name1 not in self.get_node_names():
      logging.error(f"Node: {name1} is not present in the graph to add an edge")
      sys.exit()
    if name2 not in self.get_node_names():
      logging.error(f"Node: {name2} is not present in the graph to add an edge")
      sys.exit()
    self.g[name1].append(name2)
    self.g[name1] = sorted(self.g[name1])
    self.g[name2].append(name1)
    self.g[name2] = sorted(self.g[name2])
