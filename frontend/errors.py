
def errorArrows(column:int) -> str:
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
    def __init__(self, stage, msg: str, column:int=-1, line:int=-1) -> None:
        super().__init__()
        self.stage = stage
        self.msg = msg
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        if self.column == -1:
            return errorArrows(self.column) + f'[{self.stage}] ' + f"Syntax Error : {self.msg}."
        else:
            return errorArrows(self.column) + f'[{self.stage}] ' + f"Syntax Error : {self.msg} at line {self.line}, column {self.column}."

class nameError(error):
    def __init__(self, stage, name: str, column:int, line:int) -> None:
        super().__init__()
        self.stage = stage
        self.name = name
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return errorArrows(self.column) + f'[{self.stage}] ' + f"Name Error : '{self.name}' on line {self.line} in column {self.column} is undefined."

class invalidCharacterError(error):
    def __init__(self, stage, character:str, column:int, line:int) -> None:
        super().__init__()
        self.stage = stage
        self.character = character
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return errorArrows(self.column) + f'[{self.stage}] ' + f"Invalid Character Error : Invalid character '{self.character}' on line {self.line} in column {self.column}"

class notImplementedError(error):
    def __init__(self, stage, msg, column:int=-1, line:int=-1) -> None:
        super().__init__()
        self.stage = stage
        self.msg = msg
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return errorArrows(self.column) + f'[{self.stage}] ' + f"Not Implemented Error : '{self.msg}' is not implemented."

class keyError(error):
    def __init__(self, stage, key, obj, column:int, line:int) -> None:
        super().__init__()
        self.stage = stage
        self.key = key
        self.obj = obj
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return errorArrows(self.column) + f'[{self.stage}] ' + f"Key Error : '{self.key}' is not in '{self.obj}'"
    
class typeError(error):
    def __init__(self, stage, type, column:int=-1, line:int=-1) -> None:
        super().__init__()
        self.stage = stage
        self.type = type
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return errorArrows(self.column) + f'[{self.stage}] ' + f"Type Error : '{self.type} is invalid.'"

class zeroDivisionError(error):
    def __init__(self, stage, column:int=-1, line:int=-1) -> None:
        super().__init__()
        self.stage = stage
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return errorArrows(self.column) + f'[{self.stage}] ' + f"Zero Division Error."
