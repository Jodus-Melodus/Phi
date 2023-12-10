from backend.values import *
from frontend.errors import *

from time import time, sleep
from hashlib import *
import sys

def out(arg) -> str:
    if isinstance(arg, (integerValue, stringValue, booleanValue, nullValue, realValue)):
        return arg.value
    elif isinstance(arg, objectValue):
        result = '{'
        for prop, value in arg.properties.items():
            result += f"{out(prop)}: {out(value)}, "
        return result.rstrip(', ') + '}'
    elif isinstance(arg, arrayValue):
        res = '[' + ', '.join(map(str, map(out, arg.items))) + ']'
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

def type_(arg:RuntimeValue) -> str:
    return arg.type
    
def wait(seconds) -> None:
    sleep(int(seconds.value))

def root(radicand, index) -> realValue:
    return realValue(float(float(radicand.value))**(1/float(index.value)), index.line, index.column)

def hash(data:stringValue) -> stringValue:
    d = data.value.encode('utf-8')
    return stringValue(sha256(d).hexdigest(), data.line, data.column)
