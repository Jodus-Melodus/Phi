
class RuntimeValue:
    def __init__(self) -> None:
        self.type = 'runtimeValue'


class nullValue(RuntimeValue):
    def __init__(self) -> None:
        self.type = 'nullValue'
        self.value = '_'

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })


class numberValue(RuntimeValue):
    def __init__(self, value) -> None:
        self.type = 'numberValue'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })
    
class stringValue(RuntimeValue):
    def __init__(self, value) -> None:
        import backend.builtInMethods as bim
        self.type = 'stringValue'
        self.value = value
        self.methods = {
            'length':nativeFunction(lambda args, scope : bim.stringLength(self))
        }

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })
    
    
class booleanValue(RuntimeValue):
    def __init__(self, value='F') -> None:
        self.type = 'booleanValue'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })

class arrayValue(RuntimeValue):
    def __init__(self, items:dict) -> None:
        import backend.builtInMethods as bim
        self.type = 'arrayValue'
        self.items = items
        self.methods = {
            'append':nativeFunction(lambda args, scope : bim.append(self, args[0])),
            'length':nativeFunction(lambda args, scope : bim.arrayLength(self)),
            'join':nativeFunction(lambda args, scope : bim.arrayJoin(self, args[0]))
        }

    def __repr__(self) -> str:
        return str({
            'type':self.type,
            'items':self.items,
            'methods':self.methods
        })
    

class objectValue(RuntimeValue):
    def __init__(self, properties:dict) -> None:
        self.type = 'objectValue'
        self.properties = properties

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'properties': self.properties
        })


class nativeFunction(RuntimeValue):
    def __init__(self, call) -> None:
        self.type = 'nativeFunctionValue'
        self.call = call

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'call': self.call
        })

class function(RuntimeValue):
    def __init__(self, name, parameters: list, declarationEnvironment, body: list) -> None:
        self.type = 'FunctionValue'
        self.name = name
        self.parameters = parameters
        self.declarationEnvironment = declarationEnvironment
        self.body = body

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'name': self.name,
            'parameters': self.parameters,
            'declarationEnvironment': self.declarationEnvironment,
            'body': self.body
        })
