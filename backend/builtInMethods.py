from backend.values import *
from frontend.errors import *

def append(array:arrayValue, value:RuntimeValue) -> arrayValue:
    index = len(array.items)
    array.items[index] = value
    return array

def arrayLength(array:arrayValue) -> integerValue:
    return integerValue(len(array.items))

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

def stringLength(string:stringValue) -> integerValue:
    return integerValue(len(string.value))

def stringFormat(args, string:stringValue) -> stringValue:
    output = ''
    s:str = string.value
    i = 0
    for j in s:
        if j == '~':
            output += str(args[i].value)
            i += 1
        else:
            output += j
    return stringValue(output)

def objItems(obj:objectValue) -> arrayValue:
    items = []
    for key in obj.properties:
        items.append(obj.properties[key])
    return arrayValue(items, obj.line, obj.column)