from backend.values import *
from time import time, sleep
import sys
from frontend.errors import *

def out(arg) -> str|bool:
    if isinstance(arg, (numberValue, stringValue, booleanValue, nullValue)):
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
        return f"fn {arg.name}()"
    else:
        return arg

def in_(arg:stringValue) -> stringValue:
    sys.stdout.write(arg.value)
    return stringValue(sys.stdin.readline().strip())

def now() -> numberValue:
    return numberValue(time())

def type_(arg:RuntimeValue) -> str:
    return arg.type
    
def wait(seconds) -> None:
    sleep(int(seconds.value))

def root(radicand, index) -> numberValue:
    return numberValue(float(float(radicand.value))**(1/float(index.value)))
