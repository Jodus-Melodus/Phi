from frontend.errors import error
from frontend.phi_lexer import *
from frontend.phi_parser import *
from backend.phi_interpreter import *
from backend.phi_environment import *
import json, os

ran = False

def incrementalParsing(sourceCode:str, filePath:str='', x=False):
    global ran, environment
    environment = createGlobalEnvironment(filePath=filePath)
    lexer = Lexer(sourceCode, filePath)
    tokens = lexer.tokenize()
    if isinstance(tokens, error):
        return tokens
    parser = Parser(tokens, filePath)
    ast = parser.genAST()
    if isinstance(ast, error):
        return ast

    if not ran:
        with open('ast.json', 'w') as f:
            f.write(json.dumps(json.loads(str(ast).replace("'", '"')), indent=4))
        ran = True

    if x:
        return ast
    else:
        return ''

def run(sourceCode:str, filePath:str='') -> None|error:
    ast = incrementalParsing(sourceCode, filePath, True)
    interpreter = Interpreter(filePath)
    res = interpreter.evaluate(ast, environment)
    if isinstance(res, (error, exportValue)):
        return res

if __name__ == '__main__':
    while True:
        command = input('phi > ')
        cmd, *parameters = command.split(' ')

        match cmd:
            case 'phi':
                while True:
                    code = input('run > ')
                    if not code:
                        break
                    res = run(code)
                    if isinstance(res, error):
                        print(res)
            case 'exit':
                exit()
            case 'run':
                if len(parameters) == 0:
                    print('Expected a filepath')
                elif len(parameters) == 1:
                    filePath = parameters[0]
                    if os.path.isfile(filePath):
                        with open(filePath, 'r') as f:
                            sourceCode = f.read()
                            res = run(sourceCode, filePath)
                            if isinstance(res, error):
                                print(res)
                    else:
                        print('File not found')
                else:
                    print('Too many arguments')
            case 'help':
                helpMessage = '''\
                Commands:
                ---------
                run [filepath]: Runs the code in the given file
                phi [code]: Executes the given Phi-code
                exit: Exits the program
                help: Prints this message
                '''
                print(helpMessage)
            case _:
                print(f"'{cmd}' is not a valid command")
            




