from backend.values import *
from frontend.errors import *

def append(array:arrayValue, value:RuntimeValue) -> None:
    index = len(array.items)
    array.items[index] = value
    return array

def arrayLength(array:arrayValue) -> None:
    return len(array.items)

def stringLength(string:stringValue) -> None:
    return len(string.value)