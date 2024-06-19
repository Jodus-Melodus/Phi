from frontend.Error import Error
from frontend.Lexer import *
from frontend.Parser import *
from backend.Interpreter import *
from backend.Environment import *
import json
import os

ran = False

# Parsing for the IDE to allow error checking while typing
def incremental_parsing(source_code: str, file_path: str = "", x: bool = False):
    global ran, environment
    environment = create_global_environment(None, file_path)
    lexer = Lexer(source_code, file_path)
    tokens = lexer.tokenize()

    if len(tokens) > 0 and isinstance(tokens[0], Error):
        return tokens
    
    parser = Parser(tokens, file_path)
    ast = parser.generate_AST()

    if not isinstance(ast, ProgramNode):
        return ast

    if not ran:
        with open("ast.json", 'w') as f:

            f.write(json.dumps(json.loads(str(ast)), indent=4))
        ran = True

    return ast

def run(source_code: str, file_path: str = "") -> None | Error | ExportValue:
    ast = incremental_parsing(source_code, file_path, True)
    interpreter = Interpreter(file_path)
    res = interpreter.evaluate(ast, environment)
    
    if isinstance(res, (Error, ExportValue)):
        return res
    
def debug(file_path: str) -> None:
    with open(file_path, 'r') as f:
        source_code = '\n'.join(f.readlines())

    lexer = Lexer(source_code, file_path)
    tokens = lexer.tokenize()

    print(tokens)

    if len(tokens) > 0 and isinstance(tokens[0], Error):
        return
    
    parser = Parser(tokens, file_path)
    ast = parser.generate_AST()

    print(ast)

    if not isinstance(ast, ProgramNode):
        return

    with open("ast.json", 'w') as f:
        f.write(json.dumps(json.loads(str(ast)), indent=4))
    
    env = create_global_environment(None, file_path)
    
    interpreter = Interpreter(file_path)
    result = interpreter.evaluate(ast, env)

    print(result)

if __name__ == "__main__":
    while True:
        command = input("phi > ")
        cmd, *parameters = command.split(" ")

        match cmd:
            case "phi":
                while True:
                    code = input("run > ")
                    if not code:
                        break
                    res = run(code)
                    if isinstance(res, Error):
                        print(res)
            case "exit":
                exit()
            case "run":
                if len(parameters) == 0:
                    print("Expected a filepath")
                elif len(parameters) == 1:
                    file_path = parameters[0]
                    if os.path.isfile(file_path):
                        with open(file_path, 'r') as f:
                            source_code = f.read()
                            res = run(source_code, file_path)
                            if isinstance(res, Error):
                                print(res)
                    else:
                        print("File not found")
                else:
                    print("Too many arguments")
            case "debug":
                if len(parameters) > 0:
                    debug(parameters[0])
                else:
                    print("Please provide a file path")
            case "clear" | "cls":
                os.system("cls" if os.name == "nt" else "clear")
            case "help":
                helpMessage = """\
Commands:
---------
exit                    Exits the program
help                    Prints this message
phi [code]              Executes the given Phi-code
run [filepath]          Runs the code in the given file
                """
                print(helpMessage)
            case _:
                print(f"'{cmd}' is not a valid command")
