from frontend.errors import Error
from frontend.phi_lexer import *
from frontend.phi_parser import *
from backend.phi_interpreter import *
from backend.phi_environment import *
import json
import os

ran = False

# Parsing for the IDE to allow error checking while typing
def incremental_parsing(source_code: str, file_path: str = '', x: bool = False):
    global ran, Environment
    Environment = create_global_environment(file_path)
    lexer = Lexer(source_code, file_path)
    tokens = lexer.tokenize()
    if isinstance(tokens, Error):
        return tokens
    parser = Parser(tokens, file_path)
    ast = parser.generate_AST()
    if isinstance(ast, Error):
        return ast

    if not ran:
        with open('ast.json', 'w') as f:
            f.write(json.dumps(json.loads(str(ast).replace("'", '"')), indent=4))
        ran = True

    return ast if x else ''

# Run code
def run(source_code: str, file_path: str = '') -> None | Error:
    ast = incremental_parsing(source_code, file_path, True)
    interpreter = Interpreter(file_path)
    res = interpreter.evaluate(ast, Environment)
    if isinstance(res, (Error, ExportValue)):
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
                    if isinstance(res, Error):
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
                            if isinstance(res, Error):
                                print(res)
                    else:
                        print('File not found')
                else:
                    print('Too many arguments')
            case 'help':
                helpMessage = '''\
Commands:
---------
exit                    Exits the program
help                    Prints this message
phi [code]              Executes the given Phi-code
run [filepath]          Runs the code in the given file
                '''
                print(helpMessage)
            case _:
                print(f"'{cmd}' is not a valid command")
