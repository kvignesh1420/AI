#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module maintains common data structures and functions.
"""
import logging
import sys
import numpy as np

class Node():
  """A class to represent the nodes of a graph

  Args:
    name: The name of the node
  """
  def __init__(self, name, value=None, probs=None):
    self.name = name
    self.value = value
    self.probs = probs
    self.type = "UNKNOWN"

  def __str__(self) -> str:
    return self.name

  def __repr__(self) -> str:
    return f"{self.type}({self.name}, {self.value}, {self.probs})"

  def __hash__(self) -> int:
    return hash(self.name)

class Graph():
  """A class to represent graphs along with helper functionality."""
  def __init__(self) -> None:
    self.edges = {}
    self.nodes = {}

  def get_node_names(self):
    """Return a list of node names"""
    return list(self.nodes.keys())

  def add_node(self, name, value=None, probs=None):
    """Add a node to the graph

    Args:
      name: The name of the node
      value: Value of the node
    """
    if name in self.get_node_names():
      logging.error(f"A node with the name {name} has already been added "
                    "to the graph.")
      sys.exit()
    node = Node(name=name, value=value, probs=probs)
    self.edges[name] = []
    self.nodes[name] = node

  def add_edge(self, name1, name2):
    """Add a directed edge from Node(name1,...) -> Node(name2, ...)

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
    self.edges[name1].append(name2)

  def get_encoded_node_names(self):
    """Encode node names into integers and store it along with
    the decoded mapping
    """
    self.encoding_map = {}
    self.decoding_map = {}
    for idx, node_name in enumerate(sorted(list(self.nodes))):
      self.encoding_map[node_name] = idx
      self.decoding_map[idx] = node_name
    return self.encoding_map

  def get_transition_matrix(self):
    """Create the initial probability transition matrix from
    the adjacency list representation
    """
    transition_matrix = [[0 for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]
    encoding_map = self.get_encoded_node_names()
    for node_name in self.nodes:
      transition_probs = self.nodes[node_name].probs
      neighbours = self.edges[node_name]
      if transition_probs is None:
        transition_probs = []
      else:
        if len(transition_probs) == 1:
          alpha = 1-transition_probs[0]
          expanded_transition_probs = [transition_probs[0]]
          failure_prob_splits = alpha/(len(neighbours[1:])) if len(neighbours[1:]) > 0 else 0
          for _ in neighbours[1:]:
            expanded_transition_probs.append(failure_prob_splits)
          transition_probs = expanded_transition_probs  
        if sum(transition_probs) != 1:
          sys.exit(f"Sum of transition probabilities for the node {node_name} != 1")  
      for idx, neighbour in enumerate(neighbours):
        row = encoding_map[node_name]
        column = encoding_map[neighbour]
        if transition_probs == []:
          prob = 0
        else:
          prob = transition_probs[idx]
        transition_matrix[row][column] = prob
    transition_matrix = np.array(transition_matrix)
    return transition_matrix

  def get_rewards(self):
    """Create the probability transition matrix from the adjacency list
    representation"""  
    rewards = [0 for _ in range(len(self.nodes))]
    encoding_map = self.get_encoded_node_names()
    for node_name in self.nodes:
      rewards[encoding_map[node_name]] = self.nodes[node_name].value
    rewards = np.array(rewards)  
    return rewards
