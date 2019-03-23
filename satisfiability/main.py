import sys
from generator import CodeGenerator

name = sys.argv[1] if len(sys.argv) > 1 else 'constraints.txt'
file = open(name, 'r')

content = file.read()
gen = CodeGenerator(content)

# add import statements
code = 'from pysmt.shortcuts import (Not, And, Or, Iff, Implies, Symbol, is_sat)'
code += '\n\n'

# add parsed line
for line in gen.generate_exec():
    code += line

# write to output file
name = 'output.py'
output_file = open(name, 'w')
output_file.write(code)

# exec output file
print(code)
exec(code)