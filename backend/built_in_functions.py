from backend.values import *
from frontend.errors import *

from time import time, sleep
from hashlib import *
import sys

def output(value, file_path:str='') -> str:
    if isinstance(value, (IntegerValue, BooleanValue, NullValue, RealValue)):
        return value.value
    if isinstance(value, StringValue):
        for a, b in [('\\n', '\n'), ('\\t', '\t')]:
            value.value = value.value.replace(a, b)
        return value.value
    elif isinstance(value, ObjectValue):
        result = '{'
        for prop, value in value.properties.items():
            result += f"{output(prop)}: {output(value)}, "
        return result.rstrip(', ') + '}'
    elif isinstance(value, ArrayValue):
        return '[' + ', '.join(map(str, map(output, value.items.values()))) + ']'
    elif isinstance(value, Function):
        parameters = [parameter.symbol for parameter in value.parameters]
        return f"fn {value.name}({', '.join(parameters)})"
    else:
        return value

def phi_input(file_path, arg:StringValue) -> StringValue:
    sys.stdout.write(arg.value)
    return StringValue(sys.stdin.readline().strip(), arg.line, arg.column)

def now(file_path) -> IntegerValue:
    return IntegerValue(time())

def type_(file_path, arg:RuntimeValue) -> StringValue:
    return StringValue(arg.type)
    
def wait(file_path, seconds) -> None:
    sleep(int(seconds.value))

def hash(file_path, data:StringValue) -> StringValue:
    d = data.value.encode('utf-8')
    return StringValue(sha256(d).hexdigest(), data.line, data.column)

def hard_cast_string(file_path, value:RuntimeValue) -> StringValue:
    return StringValue(value.value, value.line, value.column)

def hard_cast_integer(file_path, value:RuntimeValue) -> IntegerValue:
    try:
        v = int(value.value)
        return IntegerValue(v, value.line, value.column)
    except ValueError:
        return TypeError(file_path, "Integer Casting", value, value.column, value.line)

def hard_cast_real(file_path, value:RuntimeValue) -> RealValue:
    try:
        v = float(value.value)
        return RealValue(v, value.line, value.column)
    except ValueError:
        return TypeError(file_path, "Float Casting", value, value.column, value.line)

def read_file(file_path, value:StringValue) -> ArrayValue:    
    path = value.value
    f = open(path, 'r').readlines()
    v = {f.index(i) : StringValue(i, value.line, value.column) for i in f}

    return ArrayValue(v, value.line, value.column)