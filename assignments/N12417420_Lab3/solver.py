#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module provides an interface for
- value iterations
- policy iterations
based solver
"""

import logging
import sys
import numpy as np

class MarkovProcessSolver():
  def __init__(self, g, transition_matrix, rewards, df, max_iters, tolerance, minimize_cost):
    self.g = g
    self.transition_matrix = transition_matrix
    self.rewards = rewards
    self.df = df
    self.max_iters = max_iters
    self.tolerance = tolerance
    self.minimize_cost = minimize_cost
    self.values = self.rewards
    self.policy = self.get_policy()

  def get_policy(self):
    """Print the verbose policy"""
    policy = {}
    decoding_map = self.g.decoding_map
    for idx, row in enumerate(self.transition_matrix):
      state = decoding_map[idx]
      choice = decoding_map[np.argmax(row)]
      policy[state] = choice
    return policy

  def run(self):
    """Run the solver"""
    current_policy = self.policy
    values = self.values
    while True:
      values = self.value_iteration()
      new_policy = self.policy_iteration()
      if new_policy == current_policy:
        return new_policy, values
      current_policy = new_policy  

  def value_iteration(self):
    """Run value iteration"""
    logging.debug("Value Iteration")
    values = self.values
    logging.debug(self.transition_matrix.shape)
    for it in range(self.max_iters):
      logging.debug(f"Value Iteration: {it+1}")
      values_new = self.df*np.matmul(self.transition_matrix, values) + self.rewards
      if np.allclose(values_new, values, atol=self.tolerance, rtol=0):
        values = values_new
        break
      values = values_new
    self.values = values
    logging.debug(values)
    return values

  def policy_iteration(self):
    """Run policy iteration"""
    logging.debug("Policy Iteration")
    self.decision_node_names = []
    for node_name in self.g.nodes:
      if self.g.nodes[node_name].type == "DECISION":
        self.decision_node_names.append(node_name)

    encoding_map = self.g.encoding_map
    new_policy = {}
    for node_name in self.decision_node_names:
      neighbours = self.g.edges[node_name]
      neighbour_idx = encoding_map[neighbours[0]]
      ideal_neighbour_value = self.values[neighbour_idx]
      new_policy[node_name] = neighbours[0]
      for neighbour in neighbours[1:]:
        neighbour_idx = encoding_map[neighbour]
        neighbour_value = self.values[neighbour_idx]
        if self.minimize_cost:
          if neighbour_value < ideal_neighbour_value:
            ideal_neighbour_value = neighbour_value
            new_policy[node_name] = neighbour
        else:
          if neighbour_value > ideal_neighbour_value:
            ideal_neighbour_value = neighbour_value
            new_policy[node_name] = neighbour  
    self.update_policy_transition_matrix(policy=new_policy)      
    return new_policy

  def update_policy_transition_matrix(self, policy):
    encoding_map = self.g.encoding_map
    for node_name in self.decision_node_names:
      neighbours = self.g.edges[node_name]
      transition_probs = self.g.nodes[node_name].probs
      alpha = 1-transition_probs[0]
      choice_node_name = policy[node_name]
      failure_prob_splits = alpha/(len(neighbours[1:])) if len(neighbours[1:]) > 0 else 0
      expanded_transition_probs = [failure_prob_splits for _ in range(len(neighbours))]
      expanded_transition_probs[neighbours.index(choice_node_name)] = transition_probs[0]
      transition_probs = expanded_transition_probs  
      if sum(transition_probs) != 1:
        sys.exit("Sum of transition probabilities for the node != 1")  
      for idx, neighbour in enumerate(neighbours):
        row = encoding_map[node_name]
        column = encoding_map[neighbour]
        if transition_probs == []:
          prob = 0
        else:
          prob = transition_probs[idx]
        self.transition_matrix[row][column] = prob