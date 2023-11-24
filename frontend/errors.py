
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
            return f"Syntax error : {self.msg}"
        else:
            return f"Syntax error : {self.msg} on line {self.line} in column {self.column}"

class nameError(error):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"'{self.name}' is undefined."

class invalidCharacterError(error):
    def __init__(self, character:str, column:int, line:int) -> None:
        self.character = character
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return f"Invalid Character Errror : Invalid character '{self.character}' on line {self.line} in column {self.column}"

class notImplementedError(error):
    def __init__(self, msg) -> None:
        self.msg = msg

    def __repr__(self) -> str:
        return f"'{self.msg}' is not implemented."

class keyError(error):
    def __init__(self, key, obj) -> None:
        self.key = key
        self.obj = obj

    def __repr__(self) -> str:
        return f"Key Error : '{self.key}' is not in '{self.obj}'"