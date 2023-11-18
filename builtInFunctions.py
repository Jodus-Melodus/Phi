from values import *
from time import time, sleep


def disp(args) -> str:
    result = ''

    for arg in args:
        if isinstance(arg, (numberValue, nullValue)):
            result += f'{arg.value}'
        elif isinstance(arg, objectValue):
            temp = '{'
            for prop in arg.properties:
                temp += f"{prop} : {arg.properties[prop].value},"
            result += temp + '}'
        elif isinstance(arg, function):
            parameters = (parameter.symbol for parameter in arg.parameters)
            result += f'fn {arg.name}{tuple(parameters)}'
        elif isinstance(arg, booleanValue):
            result += 'T' if arg.value == True else 'F'
    return result

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

        
