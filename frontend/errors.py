
def errorArrows(column: int) -> str:
    out = ''
    while column-1 > 0:
        out += ' '
        column -= 1
    out += '^'
    return out + '\n'


class error:
    def __init__(self) -> None:
        pass


class syntaxError(error):
    def __init__(self, stage: str, msg: str, column: int, line: int) -> None:
        super().__init__()
        self.stage = stage
        self.msg = msg
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return f'''{errorArrows(self.column)}
[Syntax Error] Ln {self.line}, Col {self.column}:
{self.msg}
'''


class nameError(error):
    def __init__(self, stage: str, name: str, column: int, line: int) -> None:
        super().__init__()
        self.stage = stage
        self.name = name
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return f'''{errorArrows(self.column)}
[Name Error] Ln {self.line}, Col {self.column}:
'{self.name}' is not defined
'''


class invalidCharacterError(error):
    def __init__(self, stage: str, character: str, column: int, line: int) -> None:
        super().__init__()
        self.stage = stage
        self.character = character
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return f'''{errorArrows(self.column)}
[Invalid Character Error] Ln {self.line}, Col {self.column}:
'{self.character}' is not a valid character
'''


class notImplementedError(error):
    def __init__(self, stage: str, msg:str, column: int, line: int) -> None:
        super().__init__()
        self.stage = stage
        self.msg = msg
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return f'''{errorArrows(self.column)}
[Not Implemented Error] Ln {self.line}, Col {self.column}:
'{self.msg}' is not yet Implemented
'''


class keyError(error):
    def __init__(self, stage: str, key, obj, column: int, line: int) -> None:
        super().__init__()
        self.stage = stage
        self.key = key
        self.obj = obj
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return f'''{errorArrows(self.column)}
[Key Error] Ln {self.line}, Col {self.column}:
'{self.key}' is not a valid key for '{self.obj}'
'''


class typeError(error):
    def __init__(self, stage: str, type, column: int, line: int) -> None:
        super().__init__()
        self.stage = stage
        self.type = type
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return f'''{errorArrows(self.column)}
[Type Error] Ln {self.line}, Col {self.column}:
'{self.type}' is not a valid type
'''


class zeroDivisionError(error):
    def __init__(self, stage: str, column: int, line: int) -> None:
        super().__init__()
        self.stage = stage
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return f'''{errorArrows(self.column)}
[Zero Division Error] Ln {self.line}, Col {self.column}:
Cannot divide by zero
'''
