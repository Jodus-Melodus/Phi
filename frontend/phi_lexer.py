from frontend.errors import *

class TokenType:
    def __init__(self):
        self.int_value = 'intvalue'
        self.string_value = 'stringvalue'
        self.real_value = 'realvalue'
        self.anonymous = 'anonymous'

        self.binary_operation = 'binaryoperation'
        self.assignment_binary_operation = 'assignmentbinaryoperation'
        self.assignment_operator = 'assignmentoperator'

        self.equal = 'equal'
        self.not_equal = 'notequal'
        self.greater_than = 'greaterthan'
        self.greater_than_equal = 'greaterthanequal'
        self.less_than = 'lessthan'
        self.less_than_equal = 'lessthanequal'
        self._and = 'and'
        self._or = 'or'

        self.lineend = 'lineend'
        self.eof = 'eof'

        self.open_parenthesis = 'openparenthesis'
        self.close_parenthesis = 'closeparenthesis'
        self.open_brace = 'openbrace'
        self.close_brace = 'closebrace'
        self.open_bracket = 'openbracket'
        self.close_bracket = 'closebracket'
        self.colon = 'colon'
        self.comma = 'comma'
        self.period = 'period'
        self.single_quote = 'singlequote'
        self.double_quote = 'doublequote'
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
        self._del = 'del'

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
    'unknown':TT.unknown,
    'del':TT._del
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
    def __init__(self, source_code: str, file_path:str=''):
        self.file_path = file_path
        self.source_code = source_code
        self.line = 1
        self.column = 1

    def __str__(self) -> str:
        return 'Lexer'

    def eat(self) -> None:
        self.column += 1
        if self.source_code[0] == '\n':
            self.column = 0
            self.line += 1
        self.source_code = self.source_code[1:]

    def get(self) -> str:
        return self.source_code[0]

    def tokenize(self) -> list[Token]:
        tokens = []

        while len(self.source_code) > 0:
            char = self.get()
            match char:
                case ' ' | '\t':
                    self.eat()
                case '+' | '/' | '*' | '-' | '^' | '%':
                    self.eat()
                    if self.get() == '=':
                        tokens.append(
                            Token(
                                TT.assignment_binary_operation,
                                f'{char}=',
                                self.column,
                                self.line,
                            )
                        )
                        self.eat()
                    elif (char == '/') and (self.get() == '/'):
                        tokens.append(
                            Token(
                                TT.binary_operation,
                                f'{char}/',
                                self.column,
                                self.line,
                            )
                        )
                        self.eat()
                    else:
                        tokens.append(
                            Token(
                                TT.binary_operation, char, self.column, self.line
                            )
                        )
                case '\n':
                    tokens.append(Token(TT.lineend, char, self.column, self.line))
                    self.eat()
                case '(':
                    tokens.append(
                        Token(TT.open_parenthesis, char, self.column, self.line)
                    )
                    self.eat()
                case ')':
                    tokens.append(
                        Token(TT.close_parenthesis, char, self.column, self.line)
                    )
                    self.eat()
                case '{':
                    tokens.append(
                        Token(TT.open_brace, char, self.column, self.line)
                    )
                    self.eat()
                case '}':
                    tokens.append(
                        Token(TT.close_brace, char, self.column, self.line)
                    )
                    self.eat()
                case '[':
                    tokens.append(
                        Token(TT.open_bracket, char, self.column, self.line)
                    )
                    self.eat()
                case ']':
                    tokens.append(
                        Token(TT.close_bracket, char, self.column, self.line)
                    )
                    self.eat()
                case '=':
                    self.eat()
                    if self.get() == '=':
                        tokens.append(
                            Token(TT.equal, '==', self.column, self.line)
                        )
                        self.eat()
                    else:
                        tokens.append(
                            Token(
                                TT.assignment_operator,
                                char,
                                self.column,
                                self.line,
                            )
                        )
                case ':':
                    tokens.append(Token(TT.colon, char, self.column, self.line))
                    self.eat()
                case ',':
                    tokens.append(Token(TT.comma, char, self.column, self.line))
                    self.eat()
                case '.':
                    tokens.append(Token(TT.period, char, self.column, self.line))
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
                        if self.source_code == '':
                            return SyntaxError(
                                self.file_path,
                                self,
                                "Expected a '\"'",
                                self.column,
                                self.line,
                            )
                    self.eat()
                    tokens.append(
                        Token(TT.string_value, string, self.column, self.line)
                    )
                case "'":
                    self.eat()
                    string = ''
                    while self.get() != "'":
                        string += self.get()
                        self.eat()
                        if self.source_code == '':
                            return SyntaxError(
                                self.file_path,
                                self,
                                "Expected a '''",
                                self.column,
                                self.line,
                            )
                    self.eat()
                    tokens.append(
                        Token(TT.string_value, string, self.column, self.line)
                    )
                case '&':
                    tokens.append(Token(TT._and, char, self.column, self.line))
                    self.eat()
                case '|':
                    tokens.append(Token(TT._or, char, self.column, self.line))
                    self.eat()
                case '!':
                    self.eat()
                    if self.get() != '=':
                        return InvalidCharacterError(
                            self.file_path, self, char, self.column, self.line
                        )
                    tokens.append(
                        Token(TT.not_equal, f'{char}=', self.column, self.line)
                    )
                    self.eat()
                case '<':
                    self.eat()
                    if self.get() == '-':
                        self.eat()
                        tokens.append(
                            Token(TT._return, f'{char}-', self.column, self.line)
                        )
                    elif self.get() == '=':
                        self.eat()
                        tokens.append(
                            Token(
                                TT.less_than_equal,
                                f'{char}=',
                                self.column,
                                self.line,
                            )
                        )
                    else:
                        tokens.append(
                            Token(TT.less_than, char, self.column, self.line)
                        )
                case '>':
                    self.eat()
                    if self.get() == '=':
                        self.eat()
                        tokens.append(
                            Token(
                                TT.greater_than_equal,
                                f'{char}=',
                                self.column,
                                self.line,
                            )
                        )
                    else:
                        tokens.append(
                            Token(TT.greater_than, char, self.column, self.line)
                        )
                case '~':
                    self.eat()
                    tokens.append(
                        Token(TT.anonymous, char, self.column, self.line)
                    )
                case _:

                    if char in DIGITS:
                        number = ''
                        decimal = 0

                        while len(self.source_code) > 0:
                            char = self.get()
                            if char in DIGITS:
                                number += char
                            elif char == '.':
                                if decimal != 0:
                                    return SyntaxError(
                                        self.file_path,
                                        self,
                                        "Found two '.' ",
                                        self.column,
                                        self.line,
                                    )
                                number += char
                                decimal += 1
                            else:
                                break
                            self.eat()

                        if decimal == 0:
                            tokens.append(
                                Token(
                                    TT.int_value,
                                    int(number),
                                    self.column,
                                    self.line,
                                )
                            )
                        else:
                            tokens.append(
                                Token(
                                    TT.real_value,
                                    float(number),
                                    self.column,
                                    self.line,
                                )
                            )

                    elif char in ALPHABET:
                        name = ''

                        while len(self.source_code) > 0:
                            char = self.get()
                            if char in f'{ALPHABET}1234567890':
                                name += char
                            else:
                                break
                            self.eat()

                        if name in KEYWORDS:
                            tokens.append(
                                Token(KEYWORDS[name], name, self.column, self.line)
                            )
                        else:
                            tokens.append(
                                Token(TT.identifier, name, self.column, self.line)
                            )
                    else:
                        return InvalidCharacterError(
                            self.file_path, self, char, self.column, self.line
                        )

        tokens.append(Token(TT.eof, 'eof', self.column + 1, self.line))
        return tokens


if __name__ == '__main__':
    l = Lexer(input('> '))
    print(l.tokenize())
