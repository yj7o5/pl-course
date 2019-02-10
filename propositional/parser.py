from lexer import Location, Lexer
import sys

class VariableType:
    PROPOSITIONS = 0
    PROPOSITION  = 1
    ATOMIC       = 2
    MOREPROPOSITIONS = 3
    COMPOUND = 4
    CONNECTIVE = 5

'''
Input: Q

parse()
    node - Ps
        left > P
        right > MP

        node - P (test atomic | compound)
            left - atomic
        
        node - MP
            left - no node left i.e. Epsilon

Input: !Q 
                [!, Q]
    node - Ps    ^
        left > P
        right > MP
        
    node - P test atomic 0 1 or ID none
             test compound
             test atomic conn prop (2 more tokens after this) NOP only 2 available
             test LPAR prop RPAR NOP
             test NOT Proposition YES. expand Prop

             node - P
                atomic - ID

Input: P <=> Q
                

    
match as Ps
returns a node { type: P }
node
    left -> prop
    right -> m


'''

class Node:
    def __init__(self, t, v):
        self.type = t
        self.value = v

class Parser:
    def __init__(self):
        self.loc = Location(0, 0)

    def parse(self, tokenList):
        self.__currentTokens = tokenList
        self.__currentPtr = 0

        root = propositions() 

        return root

    def match(self, token):
        print token
        raise NotImplementedError

    def propositions(self):
    
        raise NotImplementedError

    def more_propositions(self):
        print sys._getframe().f_code.co_name
        raise NotImplementedError
    
    def proposition(self):
        print sys._getframe().f_code.co_name
        raise NotImplementedError

    def atomic(self):
        print sys._getframe().f_code.co_name
        raise NotImplementedError

    def compound(self):
        print sys._getframe().f_code.co_name

        raise NotImplementedError

    def connective(self):
        print sys._getframe().f_code.co_name
        raise NotImplementedError
        
    # add more methods if needed




