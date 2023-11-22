
def syntaxError(msg: str, column:int=-1, line:int=-1) -> None:
    if column == -1:
        return f"Syntax error : {msg}"
    else:
        return f"Syntax error : {msg} on line {line} in column {column}"

def nameError(name: str) -> None:
    return f"'{name}' is undefined."

def invalidCharacterError(character:str, column:int, line:int) -> None:
    return f"Invalid Character Errror : Invalid character '{character}' on line {line} in column {column}"


def notImplementedError(msg) -> None:
    return f"'{msg}' is not implemented."

def keyError(key, obj) -> None:
    return f"Key Error : '{key}' is not in '{obj}'"