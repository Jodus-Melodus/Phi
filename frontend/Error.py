import os

class Error:
    def __init__(self, file:str="", column:int=0, line:int=0) -> None:
        self.file = os.path.basename(file)
        self.column = column
        self.line = line

    def warning_message(self) -> str:
        return ""

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

###########################################################################################################

class SyntaxError(Error):
    def __init__(self, file:str, stage: str, msg: str, column: int, line: int) -> None:
        super().__init__(file, column, line)
        self.stage = stage
        self.msg = msg
        self.type = "syntaxError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Syntax Error] Ln {self.line}, Col {self.column} in {self.file}:
{self.msg}
"""

    def warning_message(self) -> str:
        return f"[Syntax Error] Ln {self.line}, Col {self.column} in {self.file}: {self.msg}"
###########################################################################################################

class NameError(Error):
    def __init__(self, file:str, stage: str, name: str, column: int, line: int) -> None:
        super().__init__(file, column, line)
        self.stage = stage
        self.name = name
        self.type = "nameError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Name Error] Ln {self.line}, Col {self.column} in {self.file}:
"{self.name}" is not defined
"""
    def warning_message(self) -> str:
        return f"[Name Error] Ln {self.line}, Col {self.column} in {self.file}: '{self.name}' is not defined"
###########################################################################################################

class InvalidCharacterError(Error):
    def __init__(self, file:str, stage: str, character: str, column: int, line: int) -> None:
        super().__init__(file, column, line)
        self.stage = stage
        self.character = character
        self.type = "invalidCharacterError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Invalid Character Error] Ln {self.line}, Col {self.column} in {self.file}:
"{self.character}" is not a valid character
"""

    def warning_message(self) -> str:
        return f"[Invalid Character Error] Ln {self.line}, Col {self.column} in {self.file}: '{self.character}' is not a valid character"

###########################################################################################################

class NotImplementedError(Error):
    def __init__(self, file:str, stage: str, msg: str, column: int, line: int) -> None:
        super().__init__(file, column, line)
        self.stage = stage
        self.msg = msg
        self.type = "notImplementedError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Not Implemented Error] Ln {self.line}, Col {self.column} in {self.file}:
"{self.msg}" is not yet Implemented
"""
    
    def warning_message(self) -> str:
        return f"[Not Implemented Error] Ln {self.line}, Col {self.column} in {self.file}: '{self.msg}' is not yet Implemented"
###########################################################################################################

class KeyError(Error):
    def __init__(self, file:str, stage: str, key, obj, column: int, line: int) -> None:
        super().__init__(file, column, line)
        self.stage = stage
        self.key = key
        self.obj = obj
        self.type = "keyError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Key Error] Ln {self.line}, Col {self.column} in {self.file}:
"{self.key}" is not a valid key for "{self.obj}"
"""
    
    def warning_message(self) -> str:
        return f"[Key Error] Ln {self.line}, Col {self.column} in {self.file}: '{self.key}'' is not a valid key for '{self.obj}'"
###########################################################################################################

class TypeError(Error):
    def __init__(self, file:str, stage: str, msg:str, column: int, line: int) -> None:
        super().__init__(file, column, line)
        self.stage = stage
        self.msg = msg
        self.type = "typeError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Type Error] Ln {self.line}, Col {self.column} in {self.file}:
{self.msg}
"""
    
    def warning_message(self) -> str:
        return f"[Type Error] Ln {self.line}, Col {self.column} in {self.file}: {self.msg}"
###########################################################################################################

class ZeroDivisionError(Error):
    def __init__(self, file:str, stage: str, column: int, line: int) -> None:
        super().__init__(file, column, line)
        self.stage = stage
        self.type = "zeroDivisionError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Zero Division Error] Ln {self.line}, Col {self.column} in {self.file}:
Cannot divide by zero
"""
    
    def warning_message(self) -> str:
        return f"[Zero Division Error] Ln {self.line}, Col {self.column} in {self.file}: Cannot divide by zero"
###########################################################################################################

class FileNotFoundError(Error):
    def __init__(self, file:str, stage: str, file_: str, column: int, line: int) -> None:
        super().__init__(file, column, line)
        self.stage = stage
        self.file_ = file_
        self.type = "fileNotFoundError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[File Not Found Error] Ln {self.line}, Col {self.column} in {self.file}:
File "{self.file_}" not found
"""
    
    def warning_message(self) -> str:
        return f"[File Not Found Error] Ln {self.line}, Col {self.column} in {self.file}: File '{self.file_}' not found"
    
###########################################################################################################

class ValueError(Error):
    def __init__(self, file: str, stage: str, value, column: int, line: int) -> None:
        super().__init__(file, column, line)
        self.stage = stage
        self.value = value
        self.type = "valueError"

    def __repr__(self) -> str:
        return f"""{self.error_arrows()}
[Value Error] Ln {self.line}, Col {self.column} in {self.file}:
Invalid value : "{self.value}"
"""
    
    def warning_message(self) -> str:
        return f"[Value Error] Ln {self.line}, Col {self.column} in {self.file}: Invalid value : '{self.value}'"
