import re
import string
UPPER_CASE = set(string.ascii_uppercase)

class Location:
    def __init__(self, line, col):
        self.col = col
        self.line = line

class TokenKind:
    ID = 0   # identifier
    LPAR = 1 # (
    RPAR = 2 # )
    NOT = 3  # !
    AND = 4  # /\
    OR = 5   # \/
    IMPLIES = 6  # =>
    IFF = 7  # <=>
    COMMA = 8 # ,
    
class Token:
    def __init__(self, loc, kind):
        self.loc = loc
        self.kind = kind

    def __str__(self):
        return str(self.kind)

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.line = 1
        self.col = 0

        self._cursor = -1
        self.cursor_value = None

    @property
    def cursor(self):
        return self._cursor
    
    @cursor.setter
    def cursor(self, value):
        self._cursor = value
        self.cursor_value = self.text[self._cursor] if value < len(self.text) else None
        
    def __advance(self):
        self.col += 1
        self.cursor += 1

        if self.cursor_value == '\n':
            self.col = 0
            self.line += 1
            self.cursor += 1

        return self.cursor_value

    def __token(self, token_kind):
        return Token(Location(self.line, self.col), token_kind)

    def __raise_error(self):
        raise SyntaxError('Invalid character at line {line} col {col}'.format(line=self.line, col=self.col))

    def flatten_tokenize(self):
        return map(lambda x: x.kind, self.tokenize())

    def tokenize(self):
        tokens = []
        
        print ">>>>>> {c} <<<<<<".format(c=self.text)

        while self.__advance() is not None:
            print "StartLoop: current_value={c} tokens={t} column={co} cursor={cur}".format(c=self.cursor_value, t=map(lambda x: x.kind, tokens), co=self.col, cur=self.cursor)

            # eat whitespace
            if self.cursor_value.isspace():
                has_space = False
                while self.cursor_value is not None and self.cursor_value.isspace():
                    self.col += 1
                    self.cursor += 1
                    has_space = True

                if has_space: 
                    self.col -= 1
                    self.cursor -= 1
                
                continue

            # Alpha [A-Z]
            if self.cursor_value.isalpha():
                has_alpha = False
                while self.cursor_value is not None and self.cursor_value.isalpha():
                    has_alpha = True
                    self.col += 1
                    self.cursor += 1
                
                if has_alpha: 
                    self.col -= 1
                    self.cursor -= 1

                tokens.append(self.__token(TokenKind.ID))
                continue
            
            # RPAR )
            if self.cursor_value == ')':
                tokens.append(self.__token(TokenKind.RPAR))
                continue

            # LPAR (
            if self.cursor_value == '(':
                tokens.append(self.__token(TokenKind.LPAR))
                continue

            # NOT !
            if self.cursor_value == '!':
                tokens.append(self.__token(TokenKind.NOT))
                continue

            # AND /\
            if self.cursor_value == '/':
                if self.text[self.cursor + 1] != '\\':
                    self.__raise_error()
                tokens.append(self.__token(TokenKind.AND))
                self.col += 1
                self.cursor += 1
                continue

            # OR \/
            if self.cursor_value == '\\':
                if self.text[self.cursor + 1] != '/':
                    self.__raise_error()
                
                tokens.append(self.__token(TokenKind.OR))
                self.col += 1
                self.cursor += 1
                continue

            # IMPLIES =>
            if self.cursor_value == '=':
                if self.text[self.cursor + 1] != '>':
                    self.__raise_error()
                
                tokens.append(self.__token(TokenKind.IMPLIES))
                self.col += 1
                self.cursor += 1
                continue

            # IFF <=>
            if self.cursor_value == '<':
                if not (self.text[self.cursor + 1] == '=' and self.text[self.cursor + 2] == '>'):
                    self.__raise_error()

                tokens.append(self.__token(TokenKind.IFF))
                
                self.col += 2
                self.cursor += 2
                continue

            # COMMA ,
            if self.cursor_value == ',':
                tokens.append(self.__token(TokenKind.COMMA))
                continue
            
            print "EndLoop: current_value={c} tokens={t} column={co} cursor={cur}".format(c=self.cursor_value, t=map(lambda x: x.kind, tokens), co=self.col, cur=self.cursor)

            raise Exception('Invalid character at Line {line}, Col {col}'.format(line=self.line, col=self.col))

        return tokens