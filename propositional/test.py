import unittest
import pprint 

from lexer import Lexer, TokenKind
from parser import Parser

class Tests(unittest.TestCase):
    def __print__(self, ast, i = 5):
        pprint.pprint(ast.__dict__, indent=i, depth=1)
        for c in ast.children: self.__print__(c, i+5)

    def test_single_token(self):
        stream = 'Q'

        tokens = Lexer(stream).tokenize()
        ast = Parser().parse(list(tokens))

        self.assertEqual(map(lambda x: x.kind, tokens), [TokenKind.ID], stream)

    def test_compound_statement(self):
        stream = '!Q'

        tokens = Lexer(stream).tokenize()
        ast = Parser().parse(list(tokens))

        self.assertEqual(map(lambda x: x.kind, tokens), [TokenKind.NOT, TokenKind.ID], stream)
    
    def test_invalid_statement(self):
        stream = ')Q'

        tokens = Lexer(stream).tokenize()

        self.assertEqual(map(lambda x: x.kind, tokens), [TokenKind.RPAR, TokenKind.ID], stream)

        with self.assertRaises(SyntaxError):
            ast = Parser().parse(list(tokens))

    def test_connective_statement(self):
        stream = 'P <=> Q'

        tokens = Lexer(stream).tokenize()
        ast = Parser().parse(tokens[:])
        
        self.assertEqual(map(lambda x: x.kind, tokens), [TokenKind.ID, TokenKind.IFF, TokenKind.ID], stream)

    def test_parenthesis_connective_statement(self):
        stream = '( P /\ Q )'
        
        tokens = Lexer(stream).tokenize()
        ast = Parser().parse(list(tokens))

        self.assertEqual(map(lambda x: x.kind, tokens), [TokenKind.LPAR, TokenKind.ID, TokenKind.AND, TokenKind.ID, TokenKind.RPAR], stream)

    def test_conn_invalid_statement(self):
        stream = '!Q)P!'

        tokens = Lexer(stream).tokenize()

        self.assertEqual(map(lambda x: x.kind, tokens), [TokenKind.NOT, TokenKind.ID, TokenKind.RPAR, TokenKind.ID, TokenKind.NOT])

        with self.assertRaises(SyntaxError):
            ast = Parser().parse(list(tokens))

    def test_multiple_statement(self):
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

unittest.main()
