from frontend.errors import error
from frontend.phi_lexer import *
from frontend.phi_parser import *
from backend.phi_interpreter import *
from backend.phi_environment import *
import json
import os

ran = False


def incrementalParsing(source_code: str, file_path: str = '', x=False):
    global ran, environment
    environment = createGlobalEnvironment(file_path)
    lexer = Lexer(source_code, file_path)
    tokens = lexer.tokenize()
    if isinstance(tokens, error):
        return tokens
    parser = Parser(tokens, file_path)
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


def run(source_code: str, file_path: str = '') -> None | error:
    ast = incrementalParsing(source_code, file_path, True)
    interpreter = Interpreter(file_path)
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
                    file_path = parameters[0]
                    if os.path.isfile(file_path):
                        with open(file_path, 'r') as f:
                            source_code = f.read()
                            res = run(source_code, file_path)
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
