import sys
from itertools import * 

from lexer import Lexer, TokenKind
from parser import Parser

file_name = sys.argv[1] if len(sys.argv) > 1 else 'sample.txt'
file = open(file_name, 'r')

content = file.read() 

print '/**************************************************/'


tokens = Lexer(content).tokenize()
parser = Parser()

for line, tokens_group in groupby(tokens, lambda x: x.loc.line):
    print 'Line #{i}'.format(i=line)
    print '----------'
    
    parser_output = None  
          
    try:
        parser_output = parser.parse(list(tokens_group))
    except SyntaxError as e:
        parser_output = 'Syntax Error at {msg}'.format(msg=e.message)

    print '{p}'.format(p=parser_output)

    print '\n'


