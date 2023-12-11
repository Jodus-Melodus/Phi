from frontend.errors import error
from frontend.phi_lexer import *
from frontend.phi_parser import *
from backend.phi_interpreter import *
from backend.phi_environment import *
import json

ran = False

def run(sourceCode:str) -> None|error:
    global ran
    environment = createGlobalEnvironment()
    lexer = Lexer(sourceCode)
    tokens = lexer.tokenize()
    if isinstance(tokens, error):
        return tokens
    parser = Parser(tokens)
    ast = parser.genAST()
    if isinstance(ast, error):
        return ast

    if not ran:
        with open('ast.json', 'w') as f:
            f.write(json.dumps(json.loads(str(ast).replace("'", '"')), indent=4))
        ran = True

    interpreter = Interpreter()
    res = interpreter.evaluate(ast, environment)
    if isinstance(res, (error, exportValue)):
        return res

if __name__ == '__main__':

    while True:
        filePath = input('> ')
        if filePath:
            break

    with open(filePath, 'r') as f:
        sourceCode = ''.join(f.readlines())

    res = run(sourceCode)
    if res:
        print(res)
