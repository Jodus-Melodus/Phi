from frontend.errors import error
from frontend.phi_lexer import *
from frontend.phi_parser import *
from backend.phi_interpreter import *
from backend.phi_environment import *

def run(sourceCode:str) -> None:
    sourceCodeList = sourceCode.split('\n')
    environment = createGlobalEnvironment()
    lexer = Lexer(sourceCode)
    tokens = lexer.tokenize()
    if isinstance(tokens, error):
        # print(sourceCodeList[tokens.line-1])
        return tokens
    parser = Parser(tokens)
    ast = parser.genAST()
    if isinstance(ast, error):
        # print(sourceCodeList[ast.line-1])
        return ast

    with open('ast.json', 'w') as f:
        f.write(str(ast).replace("'", '"'))

    interpreter = Interpreter()
    res = interpreter.evaluate(ast, environment)
    if isinstance(res, error):
        return res

if __name__ == '__main__':

    while True:
        filePath = input('> ')
        if filePath:
            break

    with open(filePath, 'r') as f:
        sourceCode = ''.join(f.readlines())

    run(sourceCode)
    
#todo fix : obj.prop.prop doesn't work becuase the interpreter only check if the obj.prop is a symbol