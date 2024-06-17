from frontend.Error import *
from frontend.TokenType import TokenType
from frontend.Token import Token

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

class Lexer:
    def __init__(self, source_code: str, file_path:str=''):
        self.file_path = file_path
        self.source_code = source_code
        self.errors = []
        self.tokens = []
        self.line = 1
        self.column = 1

    def __str__(self) -> str:
        return "Lexer"

    def eat(self) -> None:
        self.column += 1
        char = self.source_code[0]

        if char == '\n':
            self.column = 0
            self.line += 1
            
        self.source_code = self.source_code[1:]
        return char

    def get(self) -> str:
        return self.source_code[0]

    def tokenize(self) -> list[Token] | list[Error]:

        while len(self.source_code) > 0:
            char = self.get()
            match char:
                case ' ' | '\t':
                    self.eat()
                case '+' | '/' | '*' | '-' | '^' | '%':
                    self.process_binary_operators(char)
                case '\n':
                    self.tokens.append(Token(TT.lineend, self.eat(), self.column, self.line))
                case '(':
                    self.tokens.append(
                        Token(TT.open_parenthesis, self.eat(), self.column, self.line)
                    )
                case ')':
                    self.tokens.append(
                        Token(TT.close_parenthesis, self.eat(), self.column, self.line)
                    )
                case '{':
                    self.tokens.append(
                        Token(TT.open_brace, self.eat(), self.column, self.line)
                    )
                case '}':
                    self.tokens.append(
                        Token(TT.close_brace, self.eat(), self.column, self.line)
                    )
                case '[':
                    self.tokens.append(
                        Token(TT.open_bracket, self.eat(), self.column, self.line)
                    )
                case ']':
                    self.tokens.append(
                        Token(TT.close_bracket, self.eat(), self.column, self.line)
                    )
                case '=':
                    self.process_equal_sign(char)
                case ':':
                    self.tokens.append(Token(TT.colon, self.eat(), self.column, self.line))
                case ',':
                    self.tokens.append(Token(TT.comma, self.eat(), self.column, self.line))
                case '.':
                    self.tokens.append(Token(TT.period, self.eat(), self.column, self.line))
                case '#':
                    while self.get() != '\n':
                        self.eat()
                case '"':
                    self.process_string('"')
                case "'":
                    self.process_string("'")
                case '&':
                    self.tokens.append(Token(TT._and, self.eat(), self.column, self.line))
                case '|':
                    self.tokens.append(Token(TT._or, self.eat(), self.column, self.line))
                case '!':
                    self.process_exclamation_sign(char)
                case '<':
                    self.process_less_than(char)
                case '>':
                    self.process_greater_than(char)
                case '~':
                    self.tokens.append(
                        Token(TT.anonymous, self.eat(), self.column, self.line)
                    )
                case _:

                    if char in DIGITS:
                        self.process_numbers()

                    elif char in ALPHABET:
                        self.process_variables_and_identifiers()
                    else:
                        self.errors.append(InvalidCharacterError(
                            self.file_path, self, self.eat(), self.column, self.line
                        ))

        self.tokens.append(Token(TT.eof, 'eof', self.column + 1, self.line))

        return self.errors or self.tokens

    def process_greater_than(self, char):
        self.eat()
        if self.get() == '=':
            self.eat()
            self.tokens.append(
                            Token(
                                TT.greater_than_equal,
                                f'{char}=',
                                self.column,
                                self.line,
                            )
                        )
        else:
            self.tokens.append(
                            Token(TT.greater_than, char, self.column, self.line)
                        )

    def process_less_than(self, char):
        self.eat()
        if self.get() == '-':
            self.eat()
            self.tokens.append(
                            Token(TT._return, f'{char}-', self.column, self.line)
                        )
        elif self.get() == '=':
            self.eat()
            self.tokens.append(
                            Token(
                                TT.less_than_equal,
                                f'{char}=',
                                self.column,
                                self.line,
                            )
                        )
        else:
            self.tokens.append(
                            Token(TT.less_than, char, self.column, self.line)
                        )

    def process_exclamation_sign(self, char):
        self.eat()
        if self.get() != '=':
            self.errors.append(InvalidCharacterError(
                            self.file_path, self, char, self.column, self.line
                        ))
        self.tokens.append(
                        Token(TT.not_equal, f'{char}=', self.column, self.line)
                    )
        self.eat()

    def process_equal_sign(self, char):
        self.eat()
        if self.get() == '=':
            self.tokens.append(
                            Token(TT.equal, '==', self.column, self.line)
                        )
            self.eat()
        else:
            self.tokens.append(
                            Token(
                                TT.assignment_operator,
                                char,
                                self.column,
                                self.line,
                            )
                        )

    def process_binary_operators(self, char):
        self.eat()
        if self.get() == '=':
            self.tokens.append(
                            Token(
                                TT.assignment_binary_operation,
                                f'{char}=',
                                self.column,
                                self.line,
                            )
                        )
            self.eat()
        elif (char == '/') and (self.get() == '/'):
            self.tokens.append(
                            Token(
                                TT.binary_operation,
                                f'{char}/',
                                self.column,
                                self.line,
                            )
                        )
            self.eat()
        else:
            self.tokens.append(
                            Token(
                                TT.binary_operation, char, self.column, self.line
                            )
                        )

    def process_string(self, single_or_double: str):
        self.eat()

        if len(self.source_code) > 0:
            string = ''
            while len(self.source_code) > 0 and self.get() != single_or_double:
                string += self.get()
                self.eat()
                if self.source_code == '':
                    self.errors.append(SyntaxError(
                                    self.file_path,
                                    self,
                                    f"Expected a '{single_or_double}'",
                                    self.column,
                                    self.line,
                                ))
            if len(self.source_code) > 0:
                self.eat()
                self.tokens.append(
                                Token(TT.string_value, string, self.column, self.line)
                            )
            else:
                self.errors.append(SyntaxError(
                                    self.file_path,
                                    self,
                                    f"Expected a '{single_or_double}'",
                                    self.column,
                                    self.line,
                                ))
        else:
            self.errors.append(SyntaxError(
                                    self.file_path,
                                    self,
                                    f"Expected a '{single_or_double}'",
                                    self.column,
                                    self.line,
                                ))

    def process_variables_and_identifiers(self):
        name = ''

        while len(self.source_code) > 0:
            char = self.get()
            if char in f'{ALPHABET}1234567890':
                name += char
            else:
                break
            self.eat()

        if name in KEYWORDS:
            self.tokens.append(
                                Token(KEYWORDS[name], name, self.column, self.line)
                            )
        else:
            self.tokens.append(
                                Token(TT.identifier, name, self.column, self.line)
                            )

    def process_numbers(self):
        number = ''
        decimal = 0

        while len(self.source_code) > 0:
            char = self.get()
            if char in DIGITS:
                number += char
            elif char == '.':
                if decimal != 0:
                    self.errors.append(SyntaxError(
                                        self.file_path,
                                        self,
                                        "Found two '.' ",
                                        self.column,
                                        self.line,
                                    ))
                number += char
                decimal += 1
            else:
                break
            self.eat()

        if decimal == 0:
            self.tokens.append(
                                Token(
                                    TT.int_value,
                                    int(number),
                                    self.column,
                                    self.line,
                                )
                            )
        else:
            self.tokens.append(
                                Token(
                                    TT.real_value,
                                    float(number),
                                    self.column,
                                    self.line,
                                )
                            )