from frontend.phi_lexer import *
from frontend.phi_parser import *
from backend.phi_interpreter import *
from backend.phi_environment import *

environment = createGlobalEnvironment()

while True:
    filePath = input('> ')
    if filePath:
        break

with open(filePath, 'r') as f:
    sourceCode = ''.join(f.readlines())

    lexer = Lexer(sourceCode)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.genAST()

    with open('ast.json', 'w') as f:
        f.write(str(ast).replace("'", '"'))

    interpreter = interpreter()
    interpreter.evaluate(ast, environment)


#todo fix : obj.prop.prop doesn't work becuase the interpreter only check if the obj.prop is a symbol