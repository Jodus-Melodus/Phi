from backend.values import *
from frontend.errors import *


def append(array: arrayValue, value: RuntimeValue) -> arrayValue:
    newIndex = len(array.items)
    array.items[newIndex] = value
    return array


def arrayLength(array: arrayValue) -> integerValue:
    return integerValue(len(array.items))


def arrayJoin(array: arrayValue, join_character: stringValue) -> stringValue:
    if isinstance(join_character, stringValue):
        array_values = [v.value for v in array.items.values()]
        return stringValue(join_character.value.join(map(str, array_values)))
    else:
        return typeError('', 'Method', join_character, join_character.column, join_character.line)


def stringLength(string: stringValue) -> integerValue:
    return integerValue(len(string.value))


def stringFormat(args, string: stringValue) -> stringValue:
    formatted_string = ''
    s: str = string.value
    i = 0
    for j in s:
        if j == '$':
            formatted_string += str(args[i].value)
            i += 1
        else:
            formatted_string += j
    return stringValue(formatted_string)

# Objects
def objectItems(obj: objectValue) -> arrayValue:
    object_property_values = {}
    for i, key in enumerate(obj.properties):
        object_property_values[i] = obj.properties[key]
    return arrayValue(object_property_values, obj.line, obj.column)


def objectKeys(obj: objectValue) -> arrayValue:
    object_property_keys = {}
    for i, key in enumerate(obj.properties):
        object_property_keys[i] = stringValue(key, obj.line, obj.column)
    return arrayValue(object_property_keys, obj.line, obj.column)


def objectUpdate(obj: objectValue, new_properties) -> nullValue:
    if isinstance(new_properties, objectValue):
        object_new_properties = {**new_properties.properties}
        obj.properties.update(object_new_properties)
    else:
        return typeError('', 'Method', f"Expected an objectValue but received a '{new_properties.type}'", new_properties.column, new_properties.line)
    return nullValue()

def objectHasAttr(obj:objectValue, attribute):
    if isinstance(attribute, stringValue):
        attrName = attribute.value
        if attrName not in obj.properties:
            return booleanValue('F')
        else:
            return booleanValue('T')
    else:
        return typeError('', 'Method', f"Expected an stringValue but received a '{attribute.type}'", attribute.column, attribute.line)
