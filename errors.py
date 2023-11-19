
def syntaxError(msg: str, column:int, line:int) -> None:
    print(f"Syntax error : {msg} on line {line} in column {column}")
    exit()


def nameError(name: str) -> None:
    print(f"'{name}' is undefined.")
    exit()

def invalidCharacterError(character:str, column:int, line:int) -> None:
    print(f"Invalid Character Errror : Invalid character '{character}' on line {line} in column {column}")
    exit()


def notImplementedError(msg) -> None:
    print(f"'{msg}' is not implemented.")
    exit()

def keyError(key, obj) -> None:
    print(f"Key Error : '{key}' is not in {obj}")
    exit()