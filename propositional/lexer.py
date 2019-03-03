import string
import re
from collections import namedtuple

UPPER_CASE = set(string.ascii_uppercase)

class Location:
    def __init__(self, line, col):
        self.col = col
        self.line = line

class TokenKind:
    ID = "ID"   # identifier
    LPAR = "LPAR" # (
    RPAR = "RPAR" # )
    NOT = "NOT"  # !
    AND = "AND"  # /\
    OR = "OR"   # \/
    IMPLIES = "IMPLIES"  # =>
    IFF = "IFF"  # <=>
    COMMA = "COMMA" # ,
    NEWLINE = "NEWLINE" # \n
    SPACES = "SPACES" # \t or " "
    MISMATCH = "MISMATCH" # .

Token = namedtuple("Tuple", ["type", "value", "line", "col"])

token_specs = [
    (TokenKind.ID, r"[a-zA-Z]+"),
    (TokenKind.LPAR, r"[(]"),
    (TokenKind.RPAR, r"[)]"),
    (TokenKind.NOT, r"!"),
    (TokenKind.AND, r"/\\"),
    (TokenKind.OR, r"\\/"),
    (TokenKind.IMPLIES, r"=>"),
    (TokenKind.IFF, r"<=>"),
    (TokenKind.COMMA, r","),
    (TokenKind.NEWLINE, r"\n"),
    (TokenKind.SPACES, r"[ \t]+"),
    (TokenKind.MISMATCH, r".")
]

master_regex = "|".join("(?P<%s>)%s" % pair for pair in token_specs)

class Lexer:
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        compiled_regex = re.compile(master_regex)
        
        line_num = 1
        line_start = 0
        for mo in compiled_regex.finditer(self.text):

            kind = mo.lastgroup
            value = mo.group()
            column = mo.start()
            
            if (kind == TokenKind.NEWLINE):
                line_num += 1
                line_start = mo.end()
            elif (kind == TokenKind.SPACES):
                # ignore 
                continue
            elif (kind == TokenKind.MISMATCH):
                raise RuntimeError(f'({line_num}:{column}) invalid token: {value}')
            else:
                yield Token(kind, value, line_num, column)
