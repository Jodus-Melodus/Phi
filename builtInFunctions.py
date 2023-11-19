from values import *
from time import time, sleep
import sys

def out(arg) -> str:
    if isinstance(arg, (numberValue, stringValue, booleanValue, nullValue)):
        return arg.value
    elif isinstance(arg, objectValue):
        res = '{'
        for prop in arg.properties:
            res += f"{out(prop)} : {out(arg.properties[prop])}, "
        return res + '}'
    elif isinstance(arg, function):
        return f"fn {function.name}()"
    else:
        return arg

def length(arg:objectValue) -> numberValue:
    return numberValue(len(arg.properties))

def in_(arg:stringValue) -> stringValue:
    sys.stdout.write(arg.value)
    return stringValue(sys.stdin.readline().strip())

def now() -> numberValue:
    return numberValue(time())

def type_(arg) -> RuntimeValue:
    print(arg)
    if isinstance(arg, booleanValue):
        return booleanValue
    elif isinstance(arg, nullValue):
        return nullValue
    elif isinstance(arg, numberValue):
        return numberValue
    elif isinstance(arg, objectValue):
        return objectValue
    elif isinstance(arg, nativeFunction):
        return nativeFunction
    elif isinstance(arg, function):
        return function
    else:
        return type(arg)
    
def wait(seconds) -> None:
    sleep(int(seconds.value))

def root(radicand, index) -> numberValue:
    return numberValue(float(float(radicand.value))**(1/float(index.value)))
