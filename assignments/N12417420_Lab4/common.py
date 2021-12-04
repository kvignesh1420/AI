#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module maintains common data structures and functions
for implementing the algorithms.
"""
import numpy as np

def e2_distance(f1, f2):
  """Calculate the euclidean squared distance between features

  Args:
    f1: first feature vector
    f2: second feature vector

  Returns: euclidean squared distance between the two features
  """
  f1 = np.array(f1)
  f2 = np.array(f2)
  return np.round(np.sum(np.square(f1-f2)), 2)

def manh_distance(f1, f2):
  """Calculate the manhattan distance between features

  Args:
    f1: first feature vector
    f2: second feature vector

  Returns: manhattan distance between the two features
  """
  f1 = np.array(f1)
  f2 = np.array(f2)
  return np.round(np.sum(np.abs(f1-f2)), 2)
