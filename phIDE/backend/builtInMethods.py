from backend.values import *
from frontend.errors import *


def append(array: arrayValue, value: RuntimeValue) -> arrayValue:
    index = len(array.items)
    array.items[index] = value
    return array


def arrayLength(array: arrayValue) -> integerValue:
    return integerValue(len(array.items))


def arrayJoin(array: arrayValue, character: stringValue) -> stringValue:
    if isinstance(character, stringValue):
        values = [v.value for v in array.items.values()]
        return stringValue(character.value.join(map(str, values)))
    else:
        return typeError('', 'Method', character, character.column, character.line)


def stringLength(string: stringValue) -> integerValue:
    return integerValue(len(string.value))


def stringFormat(args, string: stringValue) -> stringValue:
    output = ''
    s: str = string.value
    i = 0
    for j in s:
        if j == '$':
            output += str(args[i].value)
            i += 1
        else:
            output += j
    return stringValue(output)

# Objects
def objectItems(obj: objectValue) -> arrayValue:
    items = {}
    for i, key in enumerate(obj.properties):
        items[i] = obj.properties[key]
    return arrayValue(items, obj.line, obj.column)


def objectKeys(obj: objectValue) -> arrayValue:
    items = {}
    for i, key in enumerate(obj.properties):
        items[i] = stringValue(key, obj.line, obj.column)
    return arrayValue(items, obj.line, obj.column)


def objectUpdate(obj: objectValue, arg) -> nullValue:
    if isinstance(arg, objectValue):
        newProps = {**arg.properties}
        obj.properties.update(newProps)
    else:
        return typeError('', 'Method', f"Expected an objectValue but received a '{arg.type}'", arg.column, arg.line)
    return nullValue()

def objectHasAttr(obj:objectValue, arg):
    if isinstance(arg, stringValue):
        attrName = arg.value
        if attrName not in obj.properties:
            return booleanValue('F')
        else:
            return booleanValue('T')
    else:
        return typeError('', 'Method', f"Expected an stringValue but received a '{arg.type}'", arg.column, arg.line)
