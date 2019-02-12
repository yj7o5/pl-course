from lexer import Location, Lexer, TokenKind, Token
import sys

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
        self.loc = Location(0, 0)
        self.token = None
        self.preorder_tokens = []

    def parse(self, tokenList):
        self.tokenList = tokenList

        self.token = self.__read_token()
    
        root = self.propositions()
        
        return self.preorder_tokens

    def match(self, token_kind):
        if token_kind != self.token.kind:
            self.__raise_error()
    
        self.token = self.__read_token()
        
        self.preorder_tokens.append(token_kind)

        return Node(token_kind)

    def propositions(self):
        node = Node(VariableType.PROPOSITIONS)
        self.preorder_tokens.append(node.type)

        node.children.extend([self.proposition(), self.more_propositions()])

        return node

    def more_propositions(self):

        node = Node(VariableType.MOREPROPOSITIONS)
        self.preorder_tokens.append(node.type)

        if self.token is None:
            node.children.extend([Node(VariableType.EPSILON)])
            self.preorder_tokens.append(VariableType.EPSILON)

        elif self.token.is_kind(TokenKind.COMMA):
            self.preorder_tokens.append(TokenKind.COMMA)
            node.children.extend([self.match(TokenKind.COMMA), self.propositions()])

        else: 
            self.__raise_error()

        return node
    
    def proposition(self):

        node = Node(VariableType.PROPOSITION)
        self.preorder_tokens.append(node.type)

        if self.token is None:
            self.__raise_error()

        elif self.token.is_kind(TokenKind.ID) and not VariableType.is_connective(self.__seek_next_token().kind):
            node.children.extend([self.atomic()])
        
        else: 
            node.children.extend([self.compound()])

        return node

    def atomic(self):

        node = Node(VariableType.ATOMIC)

        self.preorder_tokens.append(node.type)
        node.children.extend([self.match(TokenKind.ID)])

        return node

    def compound(self):

        node = Node(VariableType.COMPOUND)  
        self.preorder_tokens.append(node.type)

        if self.token is None:
            self.__raise_error()

        elif self.token.is_kind(TokenKind.NOT):
            node.children.extend([self.match(TokenKind.NOT), self.proposition()])

        elif self.token.is_kind(TokenKind.LPAR):
            node.children.extend([self.match(TokenKind.LPAR), self.proposition(), self.match(TokenKind.RPAR)])
        
        elif self.token.is_kind(TokenKind.ID):
            node.children.extend([self.atomic(), self.connective(), self.proposition()])

        else: 
            self.__raise_error()
        
        return node

    def connective(self):

        node = Node(VariableType.CONNECTIVE)
        self.preorder_tokens.append(node.type)

        if self.token is None or not VariableType.is_connective(self.token.kind):
            self.__raise_error()

        node.children.extend([self.match(self.token.kind)])

        return node
    
    def __raise_error(self):
        line = self.token.loc.line
        col = self.token.loc.col
        raise SyntaxError("line {l} col {c}".format(l=line, c=col))

    def __read_token(self):
        return self.tokenList.pop(0) if len(self.tokenList) > 0 else None

    def __seek_next_token(self):
        if len(self.tokenList) is 0: return Token(None, None)
        
        return self.tokenList[0]
    # add more methods if needed




