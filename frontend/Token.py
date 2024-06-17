class Token:
    def __init__(self, type: str, value: str | int | float, column: int, line: int) -> None:
        self.type = type
        self.value = value
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return f"{self.type}:{self.value}"