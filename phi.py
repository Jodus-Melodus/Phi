import phi_lexer
import phi_parser
import phi_interpreter
import phi_environment

environment = phi_environment.createGlobalEnvironment()

while True:
    filePath = input('> ')
    if filePath:
        break

with open(filePath, 'r') as f:
    sourceCode = ''.join(f.readlines())

    lexer = phi_lexer.Lexer(sourceCode)
    tokens = lexer.tokenize()
    parser = phi_parser.Parser(tokens)
    ast = parser.genAST()

    with open('ast.json', 'w') as f:
        f.write(str(ast).replace("'", '"'))

    interpreter = phi_interpreter.interpreter()
    interpreter.evaluate(ast, environment)


#todo fix : obj.prop.prop doesn't work becuase the interpreter only check if the obj.prop is a symbol