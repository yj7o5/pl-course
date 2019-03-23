from pysmt.shortcuts import (Symbol, Not, And, Or, Implies, Iff, is_sat)
from parser import VariableType, Parser
from lexer import Lexer, TokenKind

lexer_tokens = [t for t in TokenKind().__class__.__dict__.keys() if t[:1] != '_']

class CodeGenerator:
    # lowest-highest
    precedence = {TokenKind.LPAR: 5, TokenKind.NOT: 4, TokenKind.AND: 3, TokenKind.IMPLIES: 2, TokenKind.IFF: 2, TokenKind.OR: 1, TokenKind.COMMA: 0} 
    
    binary_ops = {TokenKind.AND: 'And', TokenKind.OR: 'Or', TokenKind.IMPLIES: 'Implies', TokenKind.IFF: 'Iff', TokenKind.COMMA: 'And'} 

    def __init__(self, code):
        self.sets = []
        
        for parser_tokens in Parser().parse(list(Lexer(code).tokenize())):
            tokens = filter(lambda x: x.type in lexer_tokens, parser_tokens)
            postfix_tkns = self.convert_to_postfix(tokens)
        
            self.sets.append(postfix_tkns) 

    def generate_exec(self):        
        for set in self.sets:
            variables_stack = []
            variable = None
            expression = None
            code = ""
            var_count = 0
            variables = []

            for t in set:
                if t.type == TokenKind.ID:
                    variable = t.value
                    expression = 'Symbol(\'{}\')'.format(t.value)

                elif t.type == TokenKind.NOT:
                    var_count += 1
                    variable = 'prop{}'.format(var_count)
                    expression = 'Not({})'.format(variables_stack.pop())
                            
                else:
                    r = variables_stack.pop()
                    l = variables_stack.pop()
                    var_count += 1
                    variable = 'prop{}'.format(var_count)
                    expression = '{}({}, {})'.format(self.binary_ops[t.type], l, r)

                # only do assignment once
                if variables.count(variable) == 0:
                    code += '{} = {}\n'.format(variable, expression)
                
                variables.append(variable)
                variables_stack.append(variable)
            
            expression = 'print(is_sat({}))'.format(variables_stack.pop())
            
            code += expression
            code += '\n\n'

            yield code
            
    def convert_to_postfix(self, tokens):
        output = []
        stack = []
        
        # enumerate infix tokens
        for t in tokens:
            # If ID append to output when ID token
            if (t.type == TokenKind.ID):
                output.append(t)
            
            # If "(" append to output as it
            elif (t.type == TokenKind.LPAR):
                stack.append(t)
            
            # If ")" pop from stack until "(" is encountered
            elif (t.type == TokenKind.RPAR):
                while(stack[-1:][0].type != TokenKind.LPAR):
                    item = stack.pop()
                    output.append(item)
                # pop out the remaining "("
                stack.pop()

            # Pop until a lower precendence token is hit or "(" is encounted and push current token into stack
            else:
                while ( len(stack) > 0                       and 
                        stack[-1:][0].type != TokenKind.LPAR and 
                        self.precedence[t.type] <= self.precedence[stack[-1:][0].type]
                    ):
                    
                    item = stack.pop()
                    output.append(item)
                stack.append(t)

        # add to output if stacks left with any tokens
        while(len(stack) > 0):
            output.append(stack.pop())

        return output
