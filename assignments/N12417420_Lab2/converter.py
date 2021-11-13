#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module converts the input from
BNF to CNF form
"""
import logging

import common
from yacc_parser import parser

def simplify_iff(root):
  """Simplify the root with <=> op.
  The funtionality is as follows:
  A <=> B is resolved into (A=>B) & (B=>A)

  Args:
    root: The root node of a sub-tree of type `common.Node`

  Returns:
    The root of the simplified sub-tree.
  """
  if root.type == "BinaryOp" and root.op == "<=>":
    node = common.BinaryOp("&",
            common.BinaryOp("=>", root.left, root.right),
            common.BinaryOp("=>", root.right, root.left))
    logging.debug(f"Simplified <=> : {common.tree_traversal(node)}")
    return node
  return root

def simplify_implies(root):
  """Simplify the root with => op.
  The funtionality is as follows:
  A => B is resolved into !A | B

  Args:
    root: The root node of a sub-tree of type `common.Node`

  Returns:
    The root of the simplified sub-tree.
  """
  if root.type == "BinaryOp" and root.op == "=>":
    node = common.BinaryOp("|",
            common.UnaryOp("!", root.left),
            root.right)
    logging.debug(f"Simplified => : {common.tree_traversal(node)}")
    return node
  return root

def apply_demorgans_law(root):
  """Apply demorgans law to simplify expressions
  The functionality is as follows:
  - !(A & B) is resolved into !A | !B
  - !(A | B) is resolved into !A & !B
  - !!A is resolved into A

  Args:
    root: The root node of a sub-tree of type `common.Node`

  Returns:
    The root of the simplified sub-tree.
  """
  if root.type == "UnaryOp" and root.op == "!":
    if root.target.type == "BinaryOp" and root.target.op == "&":
      node = common.BinaryOp("|",
              common.UnaryOp("!", root.target.left),
              common.UnaryOp("!", root.target.right))
      logging.debug(f"Applied demorgan's law : {common.tree_traversal(node)}")
      return node
    elif root.target.type == "BinaryOp" and root.target.op == "|":
      node = common.BinaryOp("&",
              common.UnaryOp("!", root.target.left),
              common.UnaryOp("!", root.target.right))
      logging.debug(f"Applied demorgan's law : {common.tree_traversal(node)}")
      return node
    elif root.target.type == "UnaryOp" and root.target.op == "!":
      logging.debug(f"Applied demorgan's law : {common.tree_traversal(root.target.target)}")
      return root.target.target
  return root

def apply_distribution(root):
  """Apply the distribution operation.
  The functionality is as follows:
  - A | (B & C) is resolved into (A | B) & (A | C)
  - (B & C) | A is resolved into (A | B) & (A | C)

  Args:
    root: The root node of a sub-tree of type `common.Node`

  Returns:
    The root of the simplified sub-tree.
  """
  if root.type == "BinaryOp" and root.op == "|":
    left = root.left
    right = root.right
    if right.type == "BinaryOp" and right.op == "&":
      node = common.BinaryOp("&",
              common.BinaryOp("|", left, right.left),
              common.BinaryOp("|", left, right.right))
      logging.debug(f"Applied distribution rule : {common.tree_traversal(node)}")
      return node
    elif left.type == "BinaryOp" and left.op == "&":
      node = common.BinaryOp("&",
              common.BinaryOp("|", right, left.left),
              common.BinaryOp("|", right, left.right))
      logging.debug(f"Applied distribution rule : {common.tree_traversal(node)}")
      return node
  return root

def bnf_to_cnf(root):
  """Convert from BNF to CNF form.

  Args:
    root: The root node of a sub-tree of type `common.Node`

  Returns:
    The root of the converted sub-tree.
  """
  if root.type == "BinaryOp":
    root = simplify_iff(root)
    root = simplify_implies(root)
    root = apply_demorgans_law(root)
    root = apply_distribution(root)
    root.left = bnf_to_cnf(root.left)
    root.right = bnf_to_cnf(root.right)
  elif root.type == "UnaryOp":
    root = apply_demorgans_law(root)
    if root.type == "UnaryOp":
      root.target = bnf_to_cnf(root.target)
    else: root = bnf_to_cnf(root)
  return root

def atom_and_negation_exist(sentence):
  """Check if the sentence contains a literal and it's negation.
  Such sentences are maked as resolved.

  Args:
    sentence: A CNF sentence.

  Returns:
    If sentence is resolved based on the literal and it's negation
    or not.
  """
  sentence_resolved = False
  literal_map = {}
  literals = [literal.strip() for literal in sentence.split(" ") if literal.strip()]
  for literal in literals:
    if "!" in literal:
      atom = literal.split("!")[-1]
      if atom in literal_map:
        sentence_resolved = True
        break
    else:
      atom = literal
      if f"!{atom}" in literal_map:
        sentence_resolved = True
        break
    literal_map[literal] = True
  if sentence_resolved:
    logging.debug(f"Resolved the following sentence: {sentence}")
  return sentence_resolved

def run(lines):
  """Driver function for running the BNF to CNF conversion.

  Args:
    lines: Lines of a file which contains the BNF input.

  Returns:
    The converted CNF sentences/clauses.
  """
  all_sentences = []
  for line in lines:
    if line!="" and line!="\n":
      result = parser.parse(line)
      logging.debug(f"CONVERTING SENTENCE: {line}")
      while common.tree_traversal(result) != common.tree_traversal(bnf_to_cnf(result)):
        result = bnf_to_cnf(result)
      sentences = common.tree_traversal(result).split(" & ")
      sentences = [sentence for sentence in sentences if not atom_and_negation_exist(sentence)]
      for sentence in sentences:
        sentence = sentence.replace("|", "")
        logging.debug(f"RESULT: {sentence}")
        all_sentences.append(sentence)
  return all_sentences
