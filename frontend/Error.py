import os

class Error:
    def __init__(self, file_path:str="", column:int=0, line:int=0) -> None:
        self.file_path = os.path.basename(file_path)
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return ""
    
    def error_arrows(self) -> str:
        column = self.column
        out = ""
        while column > 1:
            out += ' '
            column -= 1
        out += '^'
        return out + '\n'

class SyntaxError(Error):
    def __init__(self, file_path:str, stage: str, msg: str, column: int, line: int) -> None:
        super().__init__(file_path, column, line)
        self.stage = stage
        self.msg = msg
        self.type = "syntaxError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Syntax Error] Ln {self.line}, Col {self.column} in {self.file_path}: {self.msg}
"""

class NameError(Error):
    def __init__(self, file_path:str, stage: str, name: str, column: int, line: int) -> None:
        super().__init__(file_path, column, line)
        self.stage = stage
        self.name = name
        self.type = "nameError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Name Error] Ln {self.line}, Col {self.column} in {self.file_path}: "{self.name}" is not defined
"""

class InvalidCharacterError(Error):
    def __init__(self, file_path:str, stage: str, character: str, column: int, line: int) -> None:
        super().__init__(file_path, column, line)
        self.stage = stage
        self.character = character
        self.type = "invalidCharacterError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Invalid Character Error] Ln {self.line}, Col {self.column} in {self.file_path}: "{self.character}" is not a valid character
"""

class NotImplementedError(Error):
    def __init__(self, file_path:str, stage: str, msg: str, column: int, line: int) -> None:
        super().__init__(file_path, column, line)
        self.stage = stage
        self.msg = msg
        self.type = "notImplementedError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Not Implemented Error] Ln {self.line}, Col {self.column} in {self.file_path}: "{self.msg}" is not yet Implemented
"""

class KeyError(Error):
    def __init__(self, file_path:str, stage: str, key, obj, column: int, line: int) -> None:
        super().__init__(file_path, column, line)
        self.stage = stage
        self.key = key
        self.obj = obj
        self.type = "keyError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Key Error] Ln {self.line}, Col {self.column} in {self.file_path}: "{self.key}" is not a valid key for "{self.obj}"
"""

class TypeError(Error):
    def __init__(self, file_path:str, stage: str, msg:str, column: int, line: int) -> None:
        super().__init__(file_path, column, line)
        self.stage = stage
        self.msg = msg
        self.type = "typeError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Type Error] Ln {self.line}, Col {self.column} in {self.file_path}: {self.msg}
"""

class ZeroDivisionError(Error):
    def __init__(self, file_path:str, stage: str, column: int, line: int) -> None:
        super().__init__(file_path, column, line)
        self.stage = stage
        self.type = "zeroDivisionError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Zero Division Error] Ln {self.line}, Col {self.column} in {self.file_path}: Cannot divide by zero
"""

class File_pathNotFoundError(Error):
    def __init__(self, file_path:str, stage: str, file_path_: str, column: int, line: int) -> None:
        super().__init__(file_path, column, line)
        self.stage = stage
        self.file_path_ = file_path_
        self.type = "file_pathNotFoundError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[File_path Not Found Error] Ln {self.line}, Col {self.column} in {self.file_path}: File_path "{self.file_path_}" not found
"""

class ValueError(Error):
    def __init__(self, file_path: str, stage: str, value, column: int, line: int) -> None:
        super().__init__(file_path, column, line)
        self.stage = stage
        self.value = value
        self.type = "valueError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Value Error] Ln {self.line}, Col {self.column} in {self.file_path}: Invalid value : "{self.value}"
"""