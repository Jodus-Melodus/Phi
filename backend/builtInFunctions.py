from backend.values import *
from frontend.errors import *

from time import time, sleep
from hashlib import *
import sys
import math

def out(arg) -> str:
    if isinstance(arg, (integerValue, stringValue, booleanValue, nullValue, realValue)):
        return arg.value
    elif isinstance(arg, objectValue):
        result = '{'
        for prop, value in arg.properties.items():
            result += f"{out(prop)}: {out(value)}, "
        return result.rstrip(', ') + '}'
    elif isinstance(arg, arrayValue):
        res = '[' + ', '.join(map(str, map(out, arg.items.values()))) + ']'
        return res
    elif isinstance(arg, function):
        parameters = [parameter.symbol for parameter in arg.parameters]
        return f"fn {arg.name}({', '.join(parameters)})"
    else:
        return arg

def in_(arg:stringValue) -> stringValue:
    sys.stdout.write(arg.value)
    return stringValue(sys.stdin.readline().strip(), arg.line, arg.column)

def now() -> integerValue:
    return integerValue(time())

def type_(arg:RuntimeValue) -> stringValue:
    return stringValue(arg.type)
    
def wait(seconds) -> None:
    sleep(int(seconds.value))

def hash(data:stringValue) -> stringValue:
    d = data.value.encode('utf-8')
    return stringValue(sha256(d).hexdigest(), data.line, data.column)

def absoluteValue(value:integerValue|realValue) -> integerValue|realValue:
    if isinstance(value, integerValue):
        return integerValue(abs(value.value), value.line, value.column)
    elif isinstance(value, realValue):
        return realValue(abs(value.value), value.line, value.column)
    else:
        return typeError('Built-in Functions', value, value.column, value.line)

def _round(value:realValue) -> integerValue:
    return integerValue(round(value.value))

def _floor(value:realValue) -> integerValue:
    return integerValue(math.floor(value.value))

def _ceil(value:realValue) -> integerValue:
    return integerValue(math.ceil(value.value))

def hardCastStr(value:RuntimeValue) -> stringValue:
    return stringValue(value.value, value.line, value.column)

def hardCastInt(value:RuntimeValue) -> integerValue:
    try:
        v = int(value.value)
        return integerValue(v, value.line, value.column)
    except ValueError:
        return typeError("Integer Casting", value, value.column, value.line)

def hardCastReal(value:RuntimeValue) -> realValue:
    try:
        v = float(value.value)
        return realValue(v, value.line, value.column)
    except ValueError:
        return typeError("Float Casting", value, value.column, value.line)

