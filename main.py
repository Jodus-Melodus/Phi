from frontend.phi_lexer import *
from frontend.phi_parser import *
from backend.phi_interpreter import *
from backend.phi_environment import *

def run(sourceCode:str) -> None:
    environment = createGlobalEnvironment()
    lexer = Lexer(sourceCode)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.genAST()

    with open('ast.json', 'w') as f:
        f.write(str(ast).replace("'", '"'))

    interpreter = Interpreter()
    interpreter.evaluate(ast, environment)

if __name__ == '__main__':

    while True:
        filePath = input('> ')
        if filePath:
            break

    with open(filePath, 'r') as f:
        sourceCode = ''.join(f.readlines())

    run(sourceCode)
#todo fix : obj.prop.prop doesn't work becuase the interpreter only check if the obj.prop is a symbol