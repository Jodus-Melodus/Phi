from backend.values import *
from frontend.errors import *

def append(array:arrayValue, value:RuntimeValue) -> arrayValue:
    index = len(array.items)
    array.items[index] = value
    return array

def arrayLength(array:arrayValue) -> numberValue:
    return len(array.items)

def arrayJoin(array:arrayValue, character:stringValue) -> stringValue:
    if isinstance(character, stringValue):
        out = ''
        for value in array.items:
            v = array.items[value]
            if isinstance(v, stringValue):
                out += v.value + character.value
            else:
                return typeError('Method', v, v.column, v.line)
        return stringValue(out)
    else:
        return typeError('Method', character, character.column, character.line)

def stringLength(string:stringValue) -> numberValue:
    return len(string.value)