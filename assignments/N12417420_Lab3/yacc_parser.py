#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module defines the tokens, grammar and creates
the parser
"""

import logging
import sys

import ply.lex as lex
import ply.yacc as yacc

# Define the tokens for lexer and parser
tokens = (
  'ATOM',
  'EQUALS',
  'MOD',
  'COLON',
  'NUMBER',
  'LSQUARE',
  'RSQUARE',
  'COMMA'
)

t_EQUALS = r'\='
t_MOD = r'\%'
t_COLON = r'\:'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_COMMA = r'\,'

def t_NUMBER(t):
  r'[-+]?[0-9]*\.?[0-9]+(e[-+]?[0-9]+)?'
  return t

def t_ATOM(t):
  r'[a-zA-Z][a-zA-Z0-9]*'
  return t

t_ignore  = ' \t'

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t):
  logging.error("Encountered illegal token '%s' in input file" % t.value[0])
  sys.exit()

lexer = lex.lex(debug=False)

# Define grammar rules for yacc parser

def p_atom_reward_expression(p):
  """expression : ATOM EQUALS NUMBER"""
  p[0] = f"{p[1]} = {p[3]}"

def p_atom_probability_expression(p):
  """expression : ATOM MOD probabilities"""
  p[0] = f"{p[1]} % {p[3]}"

def p_probability_expression(p):
  """probabilities : NUMBER
                   | NUMBER probabilities
  """
  if len(p)==2:
    p[0] = f"{p[1]}"
  else:
    p[0] = f"{p[1]} {p[2]}"

def p_atom_edges_expression(p):
  """expression : ATOM COLON LSQUARE atoms RSQUARE"""
  p[0] = f"{p[1]} {p[2]} {p[3]} {p[4]} {p[5]}"

def p_atoms(p):
  """atoms : ATOM
           | ATOM COMMA atoms
  """
  if len(p)==2:
    p[0] = f"{p[1]}"
  else:
    p[0] = f"{p[1]} {p[2]} {p[3]}"

def p_error(p):
  logging.error(f"Encountered syntax error in input. "
                 "The input doesn't satisy any of the grammar rules. "
                 "Please make sure the lines in input_file is in proper format.")
  sys.exit()

parser = yacc.yacc(debug=False, write_tables=False)