from backend.values import *
from frontend.errors import *

def array_append(array: ArrayValue, value: RuntimeValue) -> ArrayValue:
    new_index = len(array.items)
    array.items[new_index] = value
    return array

def array_length(array: ArrayValue) -> IntegerValue:
    return IntegerValue(len(array.items))

def array_join(array: ArrayValue, join_character: StringValue) -> StringValue:
    if isinstance(join_character, StringValue):
        array_values = [v.value for v in array.items.values()]
        return StringValue(join_character.value.join(map(str, array_values)))
    else:
        return TypeError('', 'Method', join_character, join_character.column, join_character.line)

def string_length(string: StringValue) -> IntegerValue:
    return IntegerValue(len(string.value))

def string_format(args, string: StringValue) -> StringValue:
    formatted_string = ''
    s: str = string.value
    i = 0
    for j in s:
        if j == '$':
            formatted_string += str(args[i].value)
            i += 1
        else:
            formatted_string += j
    return StringValue(formatted_string)

# Objects
def object_items(obj: ObjectValue) -> ArrayValue:
    object_property_values = {
        i: obj.properties[key] for i, key in enumerate(obj.properties)
    }
    return ArrayValue(object_property_values, obj.line, obj.column)

def object_keys(obj: ObjectValue) -> ArrayValue:
    object_property_keys = {
        i: StringValue(key, obj.line, obj.column)
        for i, key in enumerate(obj.properties)
    }
    return ArrayValue(object_property_keys, obj.line, obj.column)

def object_update(obj: ObjectValue, new_properties) -> NullValue:
    if not isinstance(new_properties, ObjectValue):
        return TypeError('', 'Method', f"Expected an objectValue but received a '{new_properties.type}'", new_properties.column, new_properties.line)
    object_new_properties = {**new_properties.properties}
    obj.properties.update(object_new_properties)
    return NullValue()

def object_has_attribute(obj:ObjectValue, attribute):
    if not isinstance(attribute, StringValue):
        return TypeError('', 'Method', f"Expected an stringValue but received a '{attribute.type}'", attribute.column, attribute.line)
    attribute_name = attribute.value
    return (
        BooleanValue('F')
        if attribute_name not in obj.properties
        else BooleanValue('T')
    )
