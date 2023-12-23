from backend.values import *
from frontend.errors import *

from time import time, sleep
from hashlib import *
import sys

def output(value, file_path:str='') -> str:
    if isinstance(value, (integerValue, booleanValue, nullValue, realValue)):
        return value.value
    if isinstance(value, stringValue):
        for a, b in [('\\n', '\n'), ('\\t', '\t')]:
            value.value = value.value.replace(a, b)
        return value.value
    elif isinstance(value, objectValue):
        result = '{'
        for prop, value in value.properties.items():
            result += f"{output(prop)}: {output(value)}, "
        return result.rstrip(', ') + '}'
    elif isinstance(value, arrayValue):
        res = '[' + ', '.join(map(str, map(output, value.items.values()))) + ']'
        return res
    elif isinstance(value, function):
        parameters = [parameter.symbol for parameter in value.parameters]
        return f"fn {value.name}({', '.join(parameters)})"
    else:
        return value

def input(file_path, arg:stringValue) -> stringValue:
    sys.stdout.write(arg.value)
    return stringValue(sys.stdin.readline().strip(), arg.line, arg.column)

def now(file_path) -> integerValue:
    return integerValue(time())

def type_(file_path, arg:RuntimeValue) -> stringValue:
    return stringValue(arg.type)
    
def wait(file_path, seconds) -> None:
    sleep(int(seconds.value))

def hash(file_path, data:stringValue) -> stringValue:
    d = data.value.encode('utf-8')
    return stringValue(sha256(d).hexdigest(), data.line, data.column)

def hardCastStr(file_path, value:RuntimeValue) -> stringValue:
    return stringValue(value.value, value.line, value.column)

def hardCastInt(file_path, value:RuntimeValue) -> integerValue:
    try:
        v = int(value.value)
        return integerValue(v, value.line, value.column)
    except ValueError:
        return typeError(file_path, "Integer Casting", value, value.column, value.line)

def hardCastReal(file_path, value:RuntimeValue) -> realValue:
    try:
        v = float(value.value)
        return realValue(v, value.line, value.column)
    except ValueError:
        return typeError(file_path, "Float Casting", value, value.column, value.line)

def readfile_path(file_path, value:stringValue) -> arrayValue:    
    path = value.value
    f = open(path, 'r').readlines()
    v = {f.index(i) : stringValue(i, value.line, value.column) for i in f}

    return arrayValue(v, value.line, value.column)