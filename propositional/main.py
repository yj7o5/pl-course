import unittest
import pprint
import copy 

from lexer import Lexer, TokenKind
from parser import Parser

# file = open('sample.txt', 'r)
programs = [
 '( P /\ Q )',
 '( P \/ Q ) , ( X => Y )'
]

def print_tokens(file, tokens, ast_tokens):
    print 'Statement: {s}'.format(s=file)
    print 'Tokens: {t}'.format(t=map(lambda x: x.kind, tokens))
    print 'Result: {r}'.format(r=ast_tokens)

for p in programs:
    tokens = Lexer(p).tokenize()
    ast_tokens = Parser().parse(tokens[:])
    print_tokens(p, tokens, ast_tokens)

class Tests(unittest.TestCase):
    def __print__(self, ast, i = 5):
        pprint.pprint(ast.__dict__, indent=i, depth=1)
        for c in ast.children: self.__print__(c, i+5)

    def _test_single_token(self):
        stream = 'Q'

        tokens = Lexer(stream).tokenize()
        ast = Parser().parse(list(tokens))

        self.assertEqual(map(lambda x: x.kind, tokens), [TokenKind.ID], stream)

    def _test_compound_statement(self):
        stream = '!Q'

        tokens = Lexer(stream).tokenize()
        ast = Parser().parse(list(tokens))

        self.assertEqual(map(lambda x: x.kind, tokens), [TokenKind.NOT, TokenKind.ID], stream)
    
    def _test_invalid_statement(self):
        stream = ')Q'

        tokens = Lexer(stream).tokenize()

        # self.__print__(ast) 

        self.assertEqual(map(lambda x: x.kind, tokens), [TokenKind.RPAR, TokenKind.ID], stream)

        with self.assertRaises(SyntaxError):
            ast = Parser().parse(list(tokens))

    def _test_connective_statement(self):
        stream = 'P <=> Q'

        tokens = Lexer(stream).tokenize()
        ast = Parser().parse(tokens[:])
        
        self.assertEqual(map(lambda x: x.kind, tokens), [TokenKind.ID, TokenKind.IFF, TokenKind.ID], stream)

    def _test_parenthesis_connective_statement(self):
        stream = '( P /\ Q )'
        
        tokens = Lexer(stream).tokenize()
        ast = Parser().parse(list(tokens))

        self.assertEqual(map(lambda x: x.kind, tokens), [TokenKind.LPAR, TokenKind.ID, TokenKind.AND, TokenKind.ID, TokenKind.RPAR], stream)

    def _test_conn_invalid_statement(self):
        stream = '!Q)P!'

        tokens = Lexer(stream).tokenize()

        self.assertEqual(map(lambda x: x.kind, tokens), [TokenKind.NOT, TokenKind.ID, TokenKind.RPAR, TokenKind.ID, TokenKind.NOT])

        with self.assertRaises(SyntaxError):
            ast = Parser().parse(list(tokens))

    def _test_multiple_statement(self):
        stream = '( P \/ Q ) , ( X => Y )'
        
        tokens = Lexer(stream).tokenize()
        ast = Parser().parse(list(tokens))

        self.assertEqual(
            map(lambda x: x.kind, tokens),
            [
                TokenKind.LPAR, TokenKind.ID, TokenKind.OR, TokenKind.ID, TokenKind.RPAR, 
                TokenKind.COMMA,
                TokenKind.LPAR, TokenKind.ID, TokenKind.IMPLIES, TokenKind.ID, TokenKind.RPAR
            ],
            stream
        )

if __name__ == '__main__':
    unittest.main()
