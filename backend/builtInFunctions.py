from backend.values import *
from frontend.errors import *

from time import time, sleep
from hashlib import *
import sys
import math

def output(arg, file:str='') -> str:
    if isinstance(arg, (integerValue, booleanValue, nullValue, realValue)):
        return arg.value
    if isinstance(arg, stringValue):
        for a, b in [('\\n', '\n'), ('\\t', '\t')]:
            arg.value = arg.value.replace(a, b)
        return arg.value
    elif isinstance(arg, objectValue):
        result = '{'
        for prop, value in arg.properties.items():
            result += f"{output(prop)}: {output(value)}, "
        return result.rstrip(', ') + '}'
    elif isinstance(arg, arrayValue):
        res = '[' + ', '.join(map(str, map(output, arg.items.values()))) + ']'
        return res
    elif isinstance(arg, function):
        parameters = [parameter.symbol for parameter in arg.parameters]
        return f"fn {arg.name}({', '.join(parameters)})"
    else:
        return arg

def input(file, arg:stringValue) -> stringValue:
    sys.stdout.write(arg.value)
    return stringValue(sys.stdin.readline().strip(), arg.line, arg.column)

def now(file, ) -> integerValue:
    return integerValue(time())

def type_(file, arg:RuntimeValue) -> stringValue:
    return stringValue(arg.type)
    
def wait(file, seconds) -> None:
    sleep(int(seconds.value))

def hash(file, data:stringValue) -> stringValue:
    d = data.value.encode('utf-8')
    return stringValue(sha256(d).hexdigest(), data.line, data.column)

def absoluteValue(file, value:integerValue|realValue) -> integerValue|realValue:
    if isinstance(value, integerValue):
        return integerValue(abs(value.value), value.line, value.column)
    elif isinstance(value, realValue):
        return realValue(abs(value.value), value.line, value.column)
    else:
        return typeError(file, 'Built-in Functions', value, value.column, value.line)

def _round(file, value:realValue) -> integerValue:
    return integerValue(round(value.value))

def _floor(file, value:realValue) -> integerValue:
    return integerValue(math.floor(value.value))

def _ceil(file, value:realValue) -> integerValue:
    return integerValue(math.ceil(value.value))

def hardCastStr(file, value:RuntimeValue) -> stringValue:
    return stringValue(value.value, value.line, value.column)

def hardCastInt(file, value:RuntimeValue) -> integerValue:
    try:
        v = int(value.value)
        return integerValue(v, value.line, value.column)
    except ValueError:
        return typeError(file, "Integer Casting", value, value.column, value.line)

def hardCastReal(file, value:RuntimeValue) -> realValue:
    try:
        v = float(value.value)
        return realValue(v, value.line, value.column)
    except ValueError:
        return typeError(file, "Float Casting", value, value.column, value.line)

