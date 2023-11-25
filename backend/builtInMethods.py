from backend.values import *
from frontend.errors import *

def append(array:arrayValue, value:RuntimeValue) -> None:
    index = len(array.items)
    array.items[index] = value
    return array

def length(array:arrayValue) -> None:
    return len(array.items)