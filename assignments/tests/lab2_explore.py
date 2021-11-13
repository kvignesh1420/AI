import pprint
import ply.lex as lex

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

t_IFF    = r'<=>'
t_IMPLIES   = r'=>'
t_OR   = r'\|'
t_AND  = r'&'
t_NOT = r'!'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_ATOM(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     return t

def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)

t_ignore  = ' \t'
def t_error(t):
     print("Encountered illegal token '%s'" % t.value[0])
     t.lexer.skip(1)

lexer = lex.lex(debug=False)

data = """
P Q !W
!P Q
W
!P !W
"""

lexer.input(data)
for tok in lexer:
    print(tok.type, tok.value, tok.lineno, tok.lexpos)

import ply.yacc as yacc

precedence = (
     ('left', 'IFF'),
     ('left', 'IMPLIES'),
     ('left', 'OR'),
     ('left', 'AND'),
     ('right', 'NOT'),
)

class BinaryOp():
    def __init__(self, op, left, right):
        self.type = "BinaryOp"
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.type}({self.op}, {self.left}, {self.right})"

class UnaryOp():
    def __init__(self, op, target):
        self.type = "UnaryOp"
        self.target = target
        self.op = op

    def __repr__(self):
        return f"{self.type}({self.op}, {self.target})"

class Atom():
    def __init__(self, value):
        self.type = "Atom"
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})"

def p_expression(p):
    """expression : atomic_expression
                  | complex_expression
    """
    p[0] = p[1]

def p_atomic_expression(p):
    """atomic_expression : ATOM"""
    # p[0] = p[1]
    p[0] = Atom(p[1])

def p_complex_expression_paren(p):
    """complex_expression : LPAREN expression RPAREN"""
    # p[0] = f"({p[2]})"
    p[0] = p[2]

def p_complex_expression_not(p):
    """complex_expression : NOT expression"""
    # p[0] = f"!{p[2]}"
    p[0] = UnaryOp(p[1], p[2])

def p_complex_expression_and(p):
    """complex_expression : expression AND expression"""
    # p[0] = f"{p[1]} & {p[3]}"
    p[0] = BinaryOp(p[2], p[1], p[3])

def p_complex_expression_or(p):
    """complex_expression : expression OR expression"""
    # p[0] = f"{p[1]} | {p[3]}"
    p[0] = BinaryOp(p[2], p[1], p[3])

def p_complex_expression_implies(p):
    """complex_expression : expression IMPLIES expression"""
    # p[0] = f"{p[1]} => {p[3]}"
    p[0] = BinaryOp(p[2], p[1], p[3])

def p_complex_expression_iff(p):
    """complex_expression : expression IFF expression"""
    # p[0] = f"{p[1]} <=> {p[3]}"
    p[0] = BinaryOp(p[2], p[1], p[3])

def p_error(p):
     print("Syntax error in input: ", p)

def simplify_iff(root):
    if root.type == "BinaryOp" and root.op == "<=>":
        node = BinaryOp("&", BinaryOp("=>", root.left, root.right), BinaryOp("=>", root.right, root.left))
        return node
    return root

def simplify_implies(root):
    if root.type == "BinaryOp" and root.op == "=>":
        node = BinaryOp("|", UnaryOp("!", root.left), root.right)
        return node
    return root

def apply_demorgans_law(root):
    if root.type == "UnaryOp" and root.op == "!":
        if root.target.type == "BinaryOp" and root.target.op == "&":
            node = BinaryOp("|", UnaryOp("!", root.target.left), UnaryOp("!", root.target.right))
            return node
        elif root.target.type == "BinaryOp" and root.target.op == "|":
            node = BinaryOp("&", UnaryOp("!", root.target.left), UnaryOp("!", root.target.right))
            return node
        elif root.target.type == "UnaryOp" and root.target.op == "!":
            return root.target.target
    return root

def apply_distribution(root):
    if root.type == "BinaryOp" and root.op == "|":
        left = root.left
        right = root.right
        if right.type == "BinaryOp" and right.op == "&":
            node = BinaryOp("&", BinaryOp("|", left, right.left), BinaryOp("|", left, right.right))
            return node
        elif left.type == "BinaryOp" and left.op == "&":
            node = BinaryOp("&", BinaryOp("|", right, left.left), BinaryOp("|", right, left.right))
            return node
    return root

def bnf_to_cnf(root):
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

def tree_traversal(root):
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

parser = yacc.yacc(debug=False, write_tables=False)

data = """
WA_R | WA_G | WA_B
"""
all_sentences = []
for text in data.split("\n"):
    if text:
        result = parser.parse(text)
        while tree_traversal(result) != tree_traversal(bnf_to_cnf(result)):
            result = bnf_to_cnf(result)

        # print(tree_traversal(result))
        sentences = tree_traversal(result).split(" & ")
        sentences = [sentence.replace("|", "") for sentence in sentences]
        all_sentences.extend(sentences)

pprint.pprint(all_sentences)