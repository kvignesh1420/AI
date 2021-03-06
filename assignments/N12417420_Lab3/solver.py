#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module provides an interface for
value and policy iterations based markov process solver
"""

import logging
import sys
import numpy as np

class MarkovProcessSolver():
  def __init__(self, g, transition_matrix, rewards, df, max_iters, tolerance, minimize_cost):
    """Initialize the MarkovProcessSolver for value and policy iterations

    Args:
      g: An instance of `common.Graph`
      transition_matrix: The initial probability transition matrix for the states
      rewards: Rewards for the states
      df: Discount factor for future rewards
      max_iters: cutoff number of value iterations for a given policy
      tolerance: threshold for the absolute difference between current
                and old values of states before stopping the value iteration.
      minimize_cost: A boolean representing whether we want to minimize cost or
                maximize rewards.
    """
    self.g = g
    self.transition_matrix = transition_matrix
    self.rewards = rewards
    self.df = df
    self.max_iters = max_iters
    self.tolerance = tolerance
    self.minimize_cost = minimize_cost
    self.values = self.rewards
    self.decision_node_names = self.g.get_decision_node_names()
    self.policy = self.get_initial_policy()

  def get_initial_policy(self):
    """Get the initial policy from the transition matrix"""
    policy = {}
    decoding_map = self.g.decoding_map
    for idx, row in enumerate(self.transition_matrix):
      state = decoding_map[idx]
      if state not in self.decision_node_names:
        continue
      choice = decoding_map[np.argmax(row)]
      policy[state] = choice
    return policy

  def run(self):
    """Run the markov process solver using value and policy
    iterations.

    Returns:
      The ideal policy and state values
    """
    current_policy = self.policy
    values = self.values
    while True:
      values = self.value_iteration()
      new_policy = self.policy_iteration()
      if new_policy == current_policy:
        return new_policy, values
      current_policy = new_policy

  def value_iteration(self):
    """Run value iteration and return the updated values

    Returns:
      Updated values of the states
    """
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
    """Run policy iteration and the return the updated policy

    Returns:
      The new policy dictionary
    """
    logging.debug("Policy Iteration")
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
    self.update_transition_matrix(policy=new_policy)
    return new_policy

  def update_transition_matrix(self, policy):
    """Update the probability transition matrix based on new policy

    Args:
      policy: The new policy based on which the transition matrix will
        be updated.

    Returns:
      A new transition matrix
    """
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
        sys.exit(f"Sum of transition probabilities for the node {node_name} != 1")
      for idx, neighbour in enumerate(neighbours):
        row = encoding_map[node_name]
        column = encoding_map[neighbour]
        if transition_probs == []:
          prob = 0
        else:
          prob = transition_probs[idx]
        self.transition_matrix[row][column] = prob
    return self.transition_matrix