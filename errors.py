
def syntaxError(msg: str, column:int, line:int) -> None:
    print(f"Syntax error : {msg} in column {column} on line {line}")
    exit()


def nameError(name: str) -> None:
    print(f"'{name}' is undefined.")
    exit()

def invalidCharacterError(character:str, column:int, line:int) -> None:
    print(f"Invalid Character Errror : Invalid character '{character}' in column {column} on line {line}")
    exit()


def notImplementedError(msg) -> None:
    print(f"'{msg}' is not implemented.")
    exit()
