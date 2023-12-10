from frontend.errors import *


class TokenType:
    def __init__(self):
        self.intValue = 'intvalue'
        self.stringValue = 'stringvalue'
        self.realValue = 'realvalue'

        self.binaryOperation = 'binaryoperation'
        self.assignmentBinaryOperation = 'assignmentbinaryoperation'
        self.assignmentOperator = 'assignmentoperator'

        self.equal = 'equal'
        self.notequal = 'notequal'
        self.greaterThan = 'greaterthan'
        self.greaterThanEqual = 'greaterthanequal'
        self.lessThan = 'lessthan'
        self.lessThanEqual = 'lessthanequal'
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
        self.int = 'int'
        self.real = 'real'
        self.string = 'string'
        self.array = 'array'
        self.bool = 'bool'
        self.obj = 'object'
        self._lambda = 'lambda'
        self.fn = 'fn'
        self._if = 'if'
        self._else = 'else'
        self._while = 'while'
        self.do = 'do'


TT = TokenType()
DIGITS = '12345678890'
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'

KEYWORDS = {
    'fn':TT.fn,
    'if':TT._if,
    'else':TT._else,
    'while':TT._while,
    'do':TT.do,
    'int':TT.int,
    'real':TT.real,
    'str':TT.string,
    'array':TT.array,
    'bool':TT.bool,
    'obj':TT.obj,
    'lambda':TT._lambda
}

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

    def __str__(self) -> str:
        return 'Lexer'

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
                    self.eat()
                    if self.get() == '=':
                        tokens.append(Token(TT.assignmentBinaryOperation, char+'=', self.index, self.column, self.line))
                        self.eat()
                    elif (char == '/') and (self.get() == '/'):
                        tokens.append(Token(TT.binaryOperation, char + '/', self.index, self.column, self.line))
                        self.eat()
                    else:
                        tokens.append(Token(TT.binaryOperation, char, self.index, self.column, self.line))
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
                    tokens.append(Token(TT.stringValue, string, self.index, self.column, self.line))
                case "'":
                    self.eat()
                    string = ''
                    while self.get() != "'":
                        string += self.get()
                        self.eat()
                    self.eat()
                    tokens.append(Token(TT.stringValue, string, self.index, self.column, self.line))
                case '&':
                    tokens.append(Token(TT._and, char, self.index, self.column, self.line))
                    self.eat()
                case '|':
                    tokens.append(Token(TT._or, char, self.index, self.column, self.line))
                    self.eat()
                case '!':
                    self.eat()
                    if self.get() == '=':
                        tokens.append(Token(TT.notequal, char+'=', self.index, self.column, self.line))
                        self.eat()
                    else:
                        return invalidCharacterError(self, char, self.column, self.line)
                case '<':
                    self.eat()
                    if self.get() == '-':
                        self.eat()
                        tokens.append(Token(TT._return, char + '-', self.index, self.column, self.line))
                    elif self.get() == '=':
                        self.eat()
                        tokens.append(Token(TT.lessThanEqual, char + '=', self.index, self.column, self.line))
                    else:
                        tokens.append(Token(TT.lessThan, char, self.index, self.column, self.line))
                case '>':
                    self.eat()
                    if self.get() == '=':
                        self.eat()
                        tokens.append(Token(TT.greaterThanEqual, char+'=', self.index, self.column, self.line))
                    else:
                        tokens.append(Token(TT.greaterThan, char ,self.index, self.column, self.line))
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
                                    return syntaxError(self, "Found two '.' ", self.column, self.line)
                            else:
                                break
                            self.eat()

                        if decimal == 0:
                            tokens.append(Token(TT.intValue, int(number), self.index, self.column, self.line))
                        else:
                            tokens.append(Token(TT.realValue, float(number), self.index, self.column, self.line))

                    elif char in ALPHABET:
                        name = ''

                        while len(self.sourceCode) > 0:
                            char = self.get()
                            if char in ALPHABET:
                                name += char
                            else:
                                break
                            self.eat()

                        if name in KEYWORDS:
                            tokens.append(Token(KEYWORDS[name], name, self.index, self.column, self.line))
                        else:
                            tokens.append(Token(TT.identifier, name, self.index, self.column, self.line))
                    else:
                        return invalidCharacterError(self, char, self.column, self.line)
                        

        tokens.append(Token(TT.eof, 'eof', self.index + 1, self.column + 1, self.line))
        return tokens


if __name__ == '__main__':
    l = Lexer(input('> '))
    print(l.tokenize())


