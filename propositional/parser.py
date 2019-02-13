from lexer import Lexer, TokenKind, Token
import sys
import itertools 

class VariableType:
    PROPOSITIONS = "PROPOSITIONS"
    PROPOSITION  = "PROPOSITION"
    ATOMIC       = "ATOMIC"
    MOREPROPOSITIONS = "MOREPROPOSITIONS"
    COMPOUND = "COMPOUND"
    CONNECTIVE = "CONNECTIVE"
    EPSILON = "EPSILON"

    @staticmethod
    def is_connective(token_kind):
        return token_kind in (TokenKind.AND, TokenKind.OR, TokenKind.IMPLIES, TokenKind.IFF)

class Node(object):
    def __init__(self, _type):
        self.type = _type
        self.children = []

class Parser:
    def __init__(self):
        self.token = None
        self.preorder_tokens = []

    def parse(self, tokenList):
        
        for i, tokens in itertools.groupby(tokenList, lambda x: x.loc.line):
            self.currentLine = list(tokens)
            self.token = self.__read_token()
            self.propositions()

        return self.preorder_tokens

    def match(self, token_kind):
        if token_kind != self.token.kind:
            self.__raise_error()
    
        self.token = self.__read_token()
         
        self.preorder_tokens.append(token_kind)

    def propositions(self):
        self.preorder_tokens.append(VariableType.PROPOSITIONS)
        
        self.proposition()
        self.more_propositions()

    def more_propositions(self):
        self.preorder_tokens.append(VariableType.MOREPROPOSITIONS)

        if self.token is None:
            self.preorder_tokens.append(VariableType.EPSILON)

        elif self.token.is_kind(TokenKind.COMMA):
            self.match(self.token.kind) 
            self.propositions()

        else: 
            self.__raise_error()
    
    def proposition(self):
        self.preorder_tokens.append(VariableType.PROPOSITION)

        if self.token is None:
            self.__raise_error()

        elif self.token.is_kind(TokenKind.ID) and not VariableType.is_connective(self.__seek_next_token().kind):
            self.atomic()
        
        else: 
            self.compound()

    def atomic(self):
        self.preorder_tokens.append(VariableType.ATOMIC)
        self.match(TokenKind.ID)

    def compound(self):
        self.preorder_tokens.append(VariableType.COMPOUND)

        if self.token is None:
            self.__raise_error()

        elif self.token.is_kind(TokenKind.NOT):
            self.match(TokenKind.NOT)
            self.proposition()

        elif self.token.is_kind(TokenKind.LPAR):
            self.match(TokenKind.LPAR)
            self.proposition()
            self.match(TokenKind.RPAR)
        
        elif self.token.is_kind(TokenKind.ID):
            self.atomic()
            self.connective()
            self.proposition()

        else: 
            self.__raise_error()
    
    def connective(self):
        self.preorder_tokens.append(VariableType.CONNECTIVE)

        if self.token is None or not VariableType.is_connective(self.token.kind):
            self.__raise_error()

        self.match(self.token.kind)
    
    def __raise_error(self):
        raise SyntaxError(self.token.loc)

    def __read_token(self):
        return self.currentLine.pop(0) if len(self.currentLine) > 0 else None

    def __seek_next_token(self):
        return self.currentLine[0] if len(self.currentLine) > 0 else Token(None, None) 
