import unittest

from lexer import Lexer, TokenKind
from parser import Parser

class Parser_Tests(unittest.TestCase):
    

class Lexer_Tests(unittest.TestCase):
    def test_single_token(self):
        stream = 'Q'
        tokens = Lexer(stream).flatten_tokenize()

        self.assertEqual(tokens, [TokenKind.ID], stream)

    def test_compound_statement(self):
        stream = '!Q'
        tokens = Lexer(stream).flatten_tokenize()

        self.assertEqual(tokens, [TokenKind.NOT, TokenKind.ID], stream)
    
    def test_invalid_statement(self):
        stream = ')Q'
        tokens = Lexer(stream).flatten_tokenize()

        self.assertEqual(tokens, [TokenKind.RPAR, TokenKind.ID], stream)
      
    def test_connective_statement(self):
        stream = 'P <=> Q'
        tokens = Lexer(stream).flatten_tokenize()
        
        self.assertEqual(tokens, [TokenKind.ID, TokenKind.IFF, TokenKind.ID], stream)

    def test_parenthesis_connective_statement(self):
        stream = '( P /\ Q )'
        tokens = Lexer(stream).flatten_tokenize()
        
        self.assertEqual(tokens, [TokenKind.LPAR, TokenKind.ID, TokenKind.AND, TokenKind.ID, TokenKind.RPAR], stream)

    def test_lrpar_conn_invalid_statement(self):
        stream = '!Q)P!'
        tokens = Lexer(stream).flatten_tokenize()
        
        self.assertEqual(tokens, [TokenKind.NOT, TokenKind.ID, TokenKind.RPAR, TokenKind.ID, TokenKind.NOT])
        #parse_tree = Parser().parse(tokelist)
        # some assertion goes here
    
    def test_multiple_statement(self):
        stream = '( P \/ Q ) , ( X => Y )'
        tokens = Lexer(stream).flatten_tokenize()
        
        self.assertEqual(
            tokens,
            [
                TokenKind.LPAR, TokenKind.ID, TokenKind.OR, TokenKind.ID, TokenKind.RPAR, 
                TokenKind.COMMA,
                TokenKind.LPAR, TokenKind.ID, TokenKind.IMPLIES, TokenKind.ID, TokenKind.RPAR
            ],
            stream
        )

if __name__ == '__main__':
    unittest.main()
