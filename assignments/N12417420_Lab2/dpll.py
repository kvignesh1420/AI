#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module solves the CNF sentences using DPLL
"""

from yacc_parser import lexer
from copy import deepcopy
import logging
import sys

import common

class DPLL():
  """A class to solve the CNF sentences into a valid assignment
  if possible
  """
  def __init__(self, sentences):
    self.atoms = sorted(self.parse_atoms(sentences))
    self.sentences = sentences
    self.V = {atom : "UNBOUND" for atom in self.atoms}
    self.validate_sentences()

  def validate_sentences(self):
    """Validate the sentences.

    If sentences contain invalid tokens such as:
    "=>", "<=>", "&", "|", then the format is incorrect
    for the algorithm to run.
    """
    for clause in self.sentences:
      for invalid_token in ["=>", "<=>", "&", "|"]:
        if invalid_token in clause:
          logging.error(f"Invalid token: '{invalid_token}' found in line: '{clause}'"
                         " for dpll mode.\nExiting the program!")
          sys.exit()

  def run(self):
    """Driver function to solve the CNF sentences"""
    return self.solve(self.atoms, self.sentences, self.V)

  def parse_atoms(self, sentences):
    """Get all the atoms in sentences

    Args:
      sentences: list of CNF sentences.

    Returns:
      A list of atoms in all the sentences
    """
    atoms = set()
    text = "\n".join(sentences)
    lexer.input(text)
    while True:
      tok = lexer.token()
      if not tok:
        break
      if tok.type == "ATOM":
        atoms.add(tok.value)
    return atoms

  def get_literal_positions(self, sentences):
    """Get positions of literals in the sentences

    Args:
      sentences: list of CNF sentences.

    Returns:
      A dict of literals and their positions in the sentences
    """
    token_positions = []
    text = "\n".join(sentences)
    lexer.input(text)
    while True:
      tok = lexer.token()
      if not tok:
        break
      token_positions.append((tok.type, tok.value, tok.lineno, tok.lexpos))

    literal_positions = {}
    for idx, tok_pos in enumerate(token_positions):
      if tok_pos[0] == "ATOM":
        if idx == 0:
          literal_positions[tok_pos[1]] = tok_pos[2]
        elif token_positions[idx-1][0] == "NOT":
          literal_positions[f"!{tok_pos[1]}"] = tok_pos[2]
        else:
          literal_positions[tok_pos[1]] = tok_pos[2]

    return sorted(literal_positions)

  def get_atom_negation_mapping(self, atoms):
    """Helper method which returns a dictionary of atoms
    along with their negation mappings, and vice-versa.

    Args:
      atoms: A list of atoms

    Returns:
      A dict of atoms along with their negation mappings,
      and vice-versa.
    """
    atom_negation_mapping = {}
    for atom in atoms:
      atom_negation_mapping[atom] = f"!{atom}"
      atom_negation_mapping[f"!{atom}"] = atom
    return atom_negation_mapping

  def get_pure_literals(self, atoms, sentences):
    """Get a sorted list of pure literals in the sentences

    Args:
      atoms: A list of atoms to consider.
      sentences: A list of sentences to consider.

    Returns:
      A sorted list of pure literals in the sentences.
    """
    atom_negation_mapping = self.get_atom_negation_mapping(atoms)
    pure_literals = []
    literal_positions = self.get_literal_positions(sentences)
    for literal in atom_negation_mapping:
      if literal in literal_positions and atom_negation_mapping[literal] not in literal_positions:
        pure_literals.append(literal)
    pure_literals.sort(key=lambda x: x.split("!")[-1])
    return pure_literals

  def obvious_assign(self, literal, V):
    """Assign the obvious value to the literal and store in V

    Args:
      literal: The literal string
      V: The atom assignment dictionary.

    Returns:
      The atom assignment dictionary after assigning the obvious
      value to the atom corresponding to the literal.
    """
    literal = literal.strip()
    if literal in self.atoms:
      atom = literal
      V[atom] = "true"
      logging.debug(f"easy case: {atom}=true")
    elif "!" in literal:
      atom = literal.split("!")[-1]
      V[atom] = "false"
      logging.debug(f"easy case: {atom}=false")
    return V

  def get_atom(self, literal):
    """Return the atom corresponding to the literal

    Args:
      literal: A literal

    Returns:
      atom corresponding to the literal
    """
    if "!" in literal:
      return literal.strip().split("!")[-1]
    return literal.strip()

  def propagate(self, atom, sentences, V):
    """Propagate the newly assigned value of atom through
    the sentences.

    Args:
      atom: An atom in the tree.
      sentences: The list of sentences to propagate the atom value
      V: The atom assignment dictionary

    Returns:
      A list of sentences after atom propagation
    """
    new_sentences = []
    for clause in sentences:
      if (f"!{atom}" in clause and V[atom] == "false"):
        continue
      elif (f"!{atom}" in clause and V[atom] == "true"):
        clause = clause.replace(f"!{atom}", "")
        new_sentences.append(clause.strip())
      elif (atom in clause and V[atom] == "true"):
        continue
      elif (atom in clause and V[atom] == "false"):
        clause = clause.replace(atom, "")
        new_sentences.append(clause.strip())
      else:
        new_sentences.append(clause.strip())
    return new_sentences

  def solve(self, atoms, sentences, V):
    """Solve the CNF sentences using DPLL

    Args:
      atoms: A list of atoms
      sentences: A list of sentences to solve
      V: The atom assignment dictionary

    Returns:
      The final atom assignment dictionary which solved the
      sentences or "NO VALID ASSIGNMENT".
    """
    while(True):
      if len(sentences)==0:
        for atom in atoms:
          if V[atom] == "UNBOUND":
            V[atom] = "false"
            logging.debug(f"Unbound default case: {atom}=false")
        return V

      else:
        for clause in sentences:
          if clause == "":
            return "NO VALID ASSIGNMENT"

        easy_case = False
        literal_positions = self.get_literal_positions(sentences)
        for clause in sentences:
          clause = clause.strip()
          if len(clause.split(" "))==1 and clause.split(" ")[0] in literal_positions:
            literal = clause.split(" ")[0]
            V = self.obvious_assign(literal, V)
            sentences = self.propagate(self.get_atom(literal), sentences, V)
            common.print_sentences(sentences)
            easy_case = True
            break

        pure_literals = self.get_pure_literals(atoms, sentences)
        for pure_literal in pure_literals:
          V = self.obvious_assign(pure_literal, V)
          sentences = [clause for clause in sentences if pure_literal not in clause]
          common.print_sentences(sentences)
          easy_case = True

        if not easy_case:
          break

    for atom in atoms:
      if V[atom] == "UNBOUND":
        logging.debug(f"hard guess: {atom}=true")
        V[atom] = "true"
        tmp_sentences = deepcopy(sentences)
        tmp_sentences = self.propagate(atom, tmp_sentences, V)
        common.print_sentences(tmp_sentences)
        tmp_V = deepcopy(V)
        V_new = self.solve(atoms, tmp_sentences, tmp_V)
        if V_new != "NO VALID ASSIGNMENT":
          return V_new

        logging.debug(f"failed hard guess: try {atom}=false")
        V[atom] = "false"
        tmp_sentences = self.propagate(atom, sentences, V)
        common.print_sentences(tmp_sentences)
        return self.solve(atoms, tmp_sentences, V)