from frontend.errors import *


class TokenType:
    def __init__(self):
        self.int = 'int'
        self.string = 'string'
        self.real = 'real'

        self.binaryOperation = 'binaryoperation'
        self.assignmentBinaryOperation = 'assignmentbinaryoperation'
        self.assignmentOperator = 'assignmentoperator'

        self.equal = 'equal'
        self.notequal = 'notequal'
        self.greaterThan = 'greaterthan'
        self.lessThan = 'lessthan'
        self._and = 'and'
        self._or = 'or'

        self.lineend = 'lineend'
        self.eof = 'eof'

        self.openParenthesis = 'openparenthesis'
        self.closeParenthesis = 'closeparenthesis'
        self.openBrace = 'openbrace'
        self.closeBrace = 'closebrace'
        self.openBracket = 'openbracket'
        self.closeBracket = 'closebracket'
        self.colon = 'colon'
        self.comma = 'comma'
        self.period = 'period'
        self.singleQuote = 'singlequote'
        self.doubleQuote = 'doublequote'
        self._return = 'return'

        self.identifier = 'identifier'

        # keywords
        self.var = 'var'
        self.const = 'const'
        self.fn = 'fn'
        self._if = 'if'
        self._while = 'while'


TT = TokenType()
DIGITS = '12345678890'
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'


class Token:
    def __init__(self, type:str, value:str|int|float, index:int, column:int, line:int) -> None:
        self.type = type
        self.value = value
        self.index = index + len(str(value))
        self.column = column + len(str(value))
        self.line = line

    def __repr__(self) -> str:
        return f'{self.type}:{self.value}'


class Lexer:
    def __init__(self, sourceCode: str):
        self.sourceCode = sourceCode
        self.index = 0
        self.line = 1
        self.column = 1

    def eat(self) -> None:
        self.index += 1
        self.column += 1
        if self.sourceCode[0] == '\n':
            self.column = 0
            self.line += 1
        self.sourceCode = self.sourceCode[1:]

    def get(self) -> str:
        return self.sourceCode[0]

    def tokenize(self) -> list[Token]:
        tokens = []

        while len(self.sourceCode) > 0:
            char = self.get()
            match char:
                case ' ' | '\t':
                    self.eat()
                case '+' | '/' | '*' | '-' | '^' | '%':
                    tokens.append(Token(TT.binaryOperation, char, self.index, self.column, self.line))
                    self.eat()
                case '\n':
                    tokens.append(Token(TT.lineend, char, self.index, self.column, self.line))
                    self.eat()
                case '(':
                    tokens.append(Token(TT.openParenthesis, char, self.index, self.column, self.line))
                    self.eat()
                case ')':
                    tokens.append(Token(TT.closeParenthesis, char, self.index, self.column, self.line))
                    self.eat()
                case '{':
                    tokens.append(Token(TT.openBrace, char, self.index, self.column, self.line))
                    self.eat()
                case '}':
                    tokens.append(Token(TT.closeBrace, char, self.index, self.column, self.line))
                    self.eat()
                case '[':
                    tokens.append(Token(TT.openBracket, char, self.index, self.column, self.line))
                    self.eat()
                case ']':
                    tokens.append(Token(TT.closeBracket, char, self.index, self.column, self.line))
                    self.eat()
                case '=':
                    self.eat()
                    if self.get() == '=':
                        tokens.append(Token(TT.equal, '==', self.index, self.column, self.line))
                        self.eat()
                    else:
                        tokens.append(Token(TT.assignmentOperator, char, self.index, self.column, self.line))
                case ':':
                    tokens.append(Token(TT.colon, char, self.index, self.column, self.line))
                    self.eat()
                case ',':
                    tokens.append(Token(TT.comma, char, self.index, self.column, self.line))
                    self.eat()
                case '.':
                    tokens.append(Token(TT.period, char, self.index, self.column, self.line))
                    self.eat()
                case '#':
                    while self.get() != '\n':
                        self.eat()
                case '"':
                    self.eat()
                    string = ''
                    while self.get() != '"':
                        string += self.get()
                        self.eat()
                    self.eat()
                    tokens.append(Token(TT.string, string, self.index, self.column, self.line))
                case '&':
                    tokens.append(Token(TT._and, char, self.index, self.column, self.line))
                    self.eat()
                case '|':
                    tokens.append(Token(TT._or, char, self.index, self.column, self.line))
                    self.eat()
                case '!':
                    self.eat()
                    if self.get() == '=':
                        tokens.append(Token(TT.notequal, char, self.index, self.column, self.line))
                        self.eat()
                    else:
                        return invalidCharacterError(char, self.column, self.line)
                case '<':
                    self.eat()
                    if self.get() == '-':
                        self.eat()
                        tokens.append(Token(TT._return, char, self.index, self.column, self.line))
                    else:
                        tokens.append(Token(TT.lessThan, char, self.index, self.column, self.line))
                case '>':
                    tokens.append(Token(TT.greaterThan, char ,self.index, self.column, self.line))
                    self.eat()
                case _:

                    if char in DIGITS:
                        number = ''
                        decimal = 0

                        while len(self.sourceCode) > 0:
                            char = self.get()
                            if char in DIGITS:
                                number += char
                            elif char == '.':
                                if decimal == 0:
                                    number += char
                                    decimal += 1
                                else:
                                    return syntaxError("Found two '.' ")
                            else:
                                break
                            self.eat()

                        if decimal == 0:
                            tokens.append(Token(TT.int, int(number), self.index, self.column, self.line))
                        else:
                            tokens.append(Token(TT.real, float(number), self.index, self.column, self.line))

                    elif char in ALPHABET:
                        name = ''

                        while len(self.sourceCode) > 0:
                            char = self.get()
                            if char in ALPHABET:
                                name += char
                            else:
                                break
                            self.eat()

                        match name:
                            case 'var':
                                tokens.append(Token(TT.var, name, self.index, self.column, self.line))
                            case 'const':
                                tokens.append(Token(TT.const, name, self.index, self.column, self.line))
                            case 'fn':
                                tokens.append(Token(TT.fn, name, self.index, self.column, self.line))
                            case 'if':
                                tokens.append(Token(TT._if, name, self.index, self.column, self.line))
                            case 'while':
                                tokens.append(Token(TT._while, name, self.index, self.column, self.line))
                            case _:
                                tokens.append(Token(TT.identifier, name, self.index, self.column, self.line))
                    else:
                        return invalidCharacterError(char, self.column, self.line)
                        

        tokens.append(Token(TT.eof, 'eof', self.index + 1, self.column + 1, self.line))
        return tokens


if __name__ == '__main__':
    l = Lexer(input('> '))
    print(l.tokenize())


