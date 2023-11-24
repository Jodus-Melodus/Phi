
def errorArrows(column:int) -> None:
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
    def __init__(self, msg: str, column:int=-1, line:int=-1) -> None:
        self.msg = msg
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        if self.column == -1:
            return errorArrows(self.column) + f"Syntax error : {self.msg}"
        else:
            return errorArrows(self.column) + f"Syntax error : {self.msg} on line {self.line} in column {self.column}"

class nameError(error):
    def __init__(self, name: str, column:int, line:int) -> None:
        self.name = name
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return errorArrows(self.column) + f"Name Error : '{self.name}' is undefined."

class invalidCharacterError(error):
    def __init__(self, character:str, column:int, line:int) -> None:
        self.character = character
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return errorArrows(self.column) + f"Invalid Character Error : Invalid character '{self.character}' on line {self.line} in column {self.column}"

class notImplementedError(error):
    def __init__(self, msg, column:int=-1, line:int=-1) -> None:
        self.msg = msg
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return errorArrows(self.column) + f"Not Implemented Error : '{self.msg}' is not implemented."

class keyError(error):
    def __init__(self, key, obj, column:int, line:int) -> None:
        self.key = key
        self.obj = obj
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return errorArrows(self.column) + f"Key Error : '{self.key}' is not in '{self.obj}'"