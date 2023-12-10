from backend.values import *
from frontend.errors import *

from time import time, sleep
from hashlib import *
import sys

def out(arg) -> str:
    if isinstance(arg, (integerValue, stringValue, booleanValue, nullValue, realValue)):
        return arg.value
    elif isinstance(arg, objectValue):
        res = '{'
        for prop in arg.properties:
            res += f"{out(prop)} : {out(arg.properties[prop])}, "
        return res + '}'
    elif isinstance(arg, arrayValue):
        res = '['
        for item in arg.items:
            res += str(out(arg.items[item])) + ', '
        return res + ']'
    elif isinstance(arg, function):
        parameters = [parameter.symbol for parameter in arg.parameters]
        return f"fn {arg.name}({', '.join(parameters)})"
    else:
        return arg

def in_(arg:stringValue) -> stringValue:
    sys.stdout.write(arg.value)
    return stringValue(sys.stdin.readline().strip())

def now() -> integerValue:
    return integerValue(time())

def type_(arg:RuntimeValue) -> str:
    return arg.type
    
def wait(seconds) -> None:
    sleep(int(seconds.value))

def root(radicand, index) -> realValue:
    return realValue(float(float(radicand.value))**(1/float(index.value)))

def hash(data:stringValue) -> stringValue:
    d = data.value.encode('utf-8')
    return stringValue(sha256(d).hexdigest())
