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
import common

# Define the tokens for lexer and parser
tokens = (
  'ATOM',
  'IFF',
  'IMPLIES',
  'OR',
  'AND',
  'NOT',
  'LPAREN',
  'RPAREN'
)

t_IFF = r'<=>'
t_IMPLIES = r'=>'
t_OR = r'\|'
t_AND = r'&'
t_NOT = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'

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

# Define and precedence and grammar rules for yacc parser
precedence = (
  ('left', 'IFF'),
  ('left', 'IMPLIES'),
  ('left', 'OR'),
  ('left', 'AND'),
  ('right', 'NOT'),
)

def p_expression(p):
  """expression : atomic_expression
                | complex_expression
  """
  p[0] = p[1]

def p_atomic_expression(p):
  """atomic_expression : ATOM"""
  p[0] = common.Atom(p[1])

def p_complex_expression_paren(p):
  """complex_expression : LPAREN expression RPAREN"""
  p[0] = p[2]

def p_complex_expression_not(p):
  """complex_expression : NOT expression"""
  p[0] = common.UnaryOp(p[1], p[2])

def p_complex_expression_and(p):
  """complex_expression : expression AND expression"""
  p[0] = common.BinaryOp(p[2], p[1], p[3])

def p_complex_expression_or(p):
  """complex_expression : expression OR expression"""
  p[0] = common.BinaryOp(p[2], p[1], p[3])

def p_complex_expression_implies(p):
  """complex_expression : expression IMPLIES expression"""
  p[0] = common.BinaryOp(p[2], p[1], p[3])

def p_complex_expression_iff(p):
  """complex_expression : expression IFF expression"""
  p[0] = common.BinaryOp(p[2], p[1], p[3])

def p_error(p):
  logging.error(f"Encountered syntax error in input. "
                 "The input doesn't satisy any of the grammar rules. "
                 "Please make sure the input is in proper BNF format.")
  sys.exit()

parser = yacc.yacc(debug=False, write_tables=False)