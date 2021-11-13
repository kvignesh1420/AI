#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module contains the common classes and functions
"""
import logging

class Node():
  """A node in the parse tree"""
  pass

class BinaryOp(Node):
  """A class to represent a binary operation, i.e an op
  which needs two operands

  Example:
  The expression A & B can be expressed as:

  >>> left = Atom('A')
  >>> right = Atom('B')
  >>> op = BinaryOp('&', left, right)
  """
  def __init__(self, op, left, right):
    self.type = "BinaryOp"
    self.op = op
    self.left = left
    self.right = right

  def __repr__(self):
    return f"{self.type}({self.op}, {self.left}, {self.right})"

class UnaryOp(Node):
  """A class to represent a unary operation, i.e an op
  which only one operand.

  Example:
  The expression !A can be expressed as:

  >>> target = Atom('A')
  >>> op = UnaryOp('!', target)
  """
  def __init__(self, op, target):
    self.type = "UnaryOp"
    self.op = op
    self.target = target

  def __repr__(self):
    return f"{self.type}({self.op}, {self.target})"

class Atom(Node):
  """A class to represent an atom in the expression

  Example:
  The atom A expressed as:

  >>> atom = Atom('A')

  which can then be used in `UnaryOp`s or `BinaryOp`s.
  """
  def __init__(self, value):
    self.type = "Atom"
    self.value = value

  def __repr__(self):
    return f"{self.type}({self.value})"

def tree_traversal(root):
  """Traverse a tree in an in-order fashion.

  Args:
    root: The root node of a sub-tree of type `common.Node`

  Returns:
    The string containing the traversed path which is
    equivalent to the overall expression.
  """
  if root.type == "UnaryOp":
    op = root.op
    target_exp = tree_traversal(root.target)
    return f"{op}{target_exp}"
  if root.type == "BinaryOp":
    left_exp = tree_traversal(root.left)
    op = root.op
    right_exp = tree_traversal(root.right)
    return f"{left_exp} {op} {right_exp}"
  if root.type == "Atom":
    return root.value

def print_sentences(sentences):
  """print individual sentences onto the console
  in debug mode.

  Args:
    sentences: A list of sentences to print
  """
  for sentence in sentences:
    logging.debug(sentence)