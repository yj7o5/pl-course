import sys
from itertools import * 

from lexer import Lexer, TokenKind
from parser import Parser

file_name = sys.argv[1] if len(sys.argv) > 1 else 'sample.txt'
file = open(file_name, 'r')

content = file.read() 

tokens = Lexer(content).tokenize()
parser = Parser()

output = None

try:
    output = parser.parse(tokens)
except SyntaxError as e:
    output = 'Syntax Error at {line}:{col}'.format(line=e.message.line, col=e.message.col)

print output
