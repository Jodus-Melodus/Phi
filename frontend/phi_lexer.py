from frontend.errors import *


class TokenType:
    def __init__(self):
        self.intValue = 'intvalue'
        self.stringValue = 'stringvalue'
        self.realValue = 'realvalue'
        self.anonymous = 'anonymous'

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
        self._continue = 'continue'
        self.unknown = 'unknown'
        self._lambda = 'lambda'
        self._import = 'import'
        self.string = 'string'
        self.export = 'export'
        self._while = 'while'
        self._break = 'break'
        self.array = 'array'
        self.obj = 'object'
        self._else = 'else'
        self.real = 'real'
        self.bool = 'bool'
        self.each = 'each'
        self._try = 'try'
        self._for = 'for'
        self.int = 'int'
        self._if = 'if'
        self._in = 'in'
        self._as = 'as'
        self.fn = 'fn'
        self.do = 'do'
        self.catch = 'catch'
        self.throw = 'throw'
        self._case = 'case'
        self._match = 'match'


TT = TokenType()
DIGITS = '12345678890'
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-?'

KEYWORDS = {
    'fn': TT.fn,
    'if': TT._if,
    'else': TT._else,
    'while': TT._while,
    'do': TT.do,
    'int': TT.int,
    'real': TT.real,
    'str': TT.string,
    'array': TT.array,
    'bool': TT.bool,
    'obj': TT.obj,
    'lambda': TT._lambda,
    'export': TT.export,
    'import': TT._import,
    'as': TT._as,
    'break': TT._break,
    'continue': TT._continue,
    'for': TT._for,
    'each': TT.each,
    'in': TT._in,
    'try': TT._try,
    'catch': TT.catch,
    'throw':TT.throw,
    'case':TT._case,
    'match':TT._match,
    'unknown':TT.unknown
}


class Token:
    def __init__(self, type: str, value: str | int | float, column: int, line: int) -> None:
        self.type = type
        self.value = value
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return f'{self.type}:{self.value}'


class Lexer:
    def __init__(self, sourceCode: str, filePath:str=''):
        self.filePath = filePath
        self.sourceCode = sourceCode
        self.line = 1
        self.column = 1

    def __str__(self) -> str:
        return 'Lexer'

    def eat(self) -> None:
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
                        tokens.append(Token(
                            TT.assignmentBinaryOperation, char+'=', self.column, self.line))
                        self.eat()
                    elif (char == '/') and (self.get() == '/'):
                        tokens.append(
                            Token(TT.binaryOperation, char + '/', self.column, self.line))
                        self.eat()
                    else:
                        tokens.append(
                            Token(TT.binaryOperation, char, self.column, self.line))
                case '\n':
                    tokens.append(
                        Token(TT.lineend, char, self.column, self.line))
                    self.eat()
                case '(':
                    tokens.append(Token(TT.openParenthesis, char,
                                  self.column, self.line))
                    self.eat()
                case ')':
                    tokens.append(Token(TT.closeParenthesis, char,
                                  self.column, self.line))
                    self.eat()
                case '{':
                    tokens.append(Token(TT.openBrace, char,
                                  self.column, self.line))
                    self.eat()
                case '}':
                    tokens.append(Token(TT.closeBrace, char,
                                  self.column, self.line))
                    self.eat()
                case '[':
                    tokens.append(Token(TT.openBracket, char,
                                  self.column, self.line))
                    self.eat()
                case ']':
                    tokens.append(Token(TT.closeBracket, char,
                                  self.column, self.line))
                    self.eat()
                case '=':
                    self.eat()
                    if self.get() == '=':
                        tokens.append(
                            Token(TT.equal, '==', self.column, self.line))
                        self.eat()
                    else:
                        tokens.append(Token(TT.assignmentOperator,
                                      char, self.column, self.line))
                case ':':
                    tokens.append(
                        Token(TT.colon, char, self.column, self.line))
                    self.eat()
                case ',':
                    tokens.append(
                        Token(TT.comma, char, self.column, self.line))
                    self.eat()
                case '.':
                    tokens.append(
                        Token(TT.period, char, self.column, self.line))
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
                        if self.sourceCode == '':
                            return syntaxError(self.filePath, self, "Expected a '\"'", self.column, self.line)
                    self.eat()
                    tokens.append(Token(TT.stringValue, string,
                                  self.column, self.line))
                case "'":
                    self.eat()
                    string = ''
                    while self.get() != "'":
                        string += self.get()
                        self.eat()
                        if self.sourceCode == '':
                            return syntaxError(self.filePath, self, "Expected a '''", self.column, self.line)
                    self.eat()
                    tokens.append(Token(TT.stringValue, string,
                                  self.column, self.line))
                case '&':
                    tokens.append(
                        Token(TT._and, char, self.column, self.line))
                    self.eat()
                case '|':
                    tokens.append(
                        Token(TT._or, char, self.column, self.line))
                    self.eat()
                case '!':
                    self.eat()
                    if self.get() == '=':
                        tokens.append(Token(TT.notequal, char+'=',
                                      self.column, self.line))
                        self.eat()
                    else:
                        return invalidCharacterError(self.filePath, self, char, self.column, self.line)
                case '<':
                    self.eat()
                    if self.get() == '-':
                        self.eat()
                        tokens.append(Token(TT._return, char + '-',
                                      self.column, self.line))
                    elif self.get() == '=':
                        self.eat()
                        tokens.append(
                            Token(TT.lessThanEqual, char + '=', self.column, self.line))
                    else:
                        tokens.append(
                            Token(TT.lessThan, char, self.column, self.line))
                case '>':
                    self.eat()
                    if self.get() == '=':
                        self.eat()
                        tokens.append(
                            Token(TT.greaterThanEqual, char+'=', self.column, self.line))
                    else:
                        tokens.append(Token(TT.greaterThan, char,
                                      self.column, self.line))
                case '~':
                    self.eat()
                    tokens.append(Token(TT.anonymous, char,
                                  self.column, self.line))
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
                                    return syntaxError(self.filePath, self, "Found two '.' ", self.column, self.line)
                            else:
                                break
                            self.eat()

                        if decimal == 0:
                            tokens.append(Token(TT.intValue, int(
                                number), self.column, self.line))
                        else:
                            tokens.append(Token(TT.realValue, float(
                                number), self.column, self.line))

                    elif char in ALPHABET:
                        name = ''

                        while len(self.sourceCode) > 0:
                            char = self.get()
                            if char in ALPHABET + '1234567890':
                                name += char
                            else:
                                break
                            self.eat()

                        if name in KEYWORDS:
                            tokens.append(
                                Token(KEYWORDS[name], name, self.column, self.line))
                        else:
                            tokens.append(
                                Token(TT.identifier, name, self.column, self.line))
                    else:
                        return invalidCharacterError(self.filePath, self, char, self.column, self.line)

        tokens.append(Token(TT.eof, 'eof', self.column + 1, self.line))
        return tokens


if __name__ == '__main__':
    l = Lexer(input('> '))
    print(l.tokenize())
