

class RuntimeValue:
    def __init__(self, line: int = -1, column: int = -1) -> None:
        self.line = line
        self.column = column
        self.type = 'runtimeValue'


class nullValue(RuntimeValue):
    def __init__(self) -> None:
        super().__init__()
        self.type = 'nullValue'
        self.value = '_'

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })
    

class unknownValue(RuntimeValue):
    def __init__(self, value, line:int=-1, column:int=-1) -> None:
        super().__init__()
        self.type = 'unknownValue'
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })


class integerValue(RuntimeValue):
    def __init__(self, value, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.type = 'integerValue'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })


class realValue(RuntimeValue):
    def __init__(self, value, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.type = 'realValue'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })


class stringValue(RuntimeValue):
    def __init__(self, value:str, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        import backend.builtInMethods as bim
        self.type = 'stringValue'
        self.value = value
        self.methods = {
            'length': nativeFunction(lambda args, scope: bim.stringLength(self)),
            'format': nativeFunction(lambda args, scope: bim.stringFormat(args, self))
        }

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })


class booleanValue(RuntimeValue):
    def __init__(self, value='F') -> None:
        super().__init__()
        self.type = 'booleanValue'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })


class arrayValue(RuntimeValue):
    def __init__(self, items: dict, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        import backend.builtInMethods as bim
        self.type = 'arrayValue'
        self.items = items
        self.methods = {
            'append': nativeFunction(lambda args, scope: bim.append(self, args[0])),
            'length': nativeFunction(lambda args, scope: bim.arrayLength(self)),
            'join': nativeFunction(lambda args, scope: bim.arrayJoin(self, args[0]))
        }

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'items': self.items,
            'methods': self.methods
        })


class objectValue(RuntimeValue):
    def __init__(self, properties: dict, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        import backend.builtInMethods as bim
        self.type = 'objectValue'
        self.properties = properties
        self.methods = {
            'items': nativeFunction(lambda args, scope: bim.objectItems(self)),
            'keys': nativeFunction(lambda args, scope: bim.objectKeys(self)),
            'update': nativeFunction(lambda args, scope: bim.objectUpdate(self, args[0])),
            'hasAttr': nativeFunction(lambda args, scope: bim.objectHasAttr(self, args[0]))
        }

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'properties': self.properties
        })


class nativeFunction(RuntimeValue):
    def __init__(self, call) -> None:
        super().__init__()
        self.type = 'nativeFunctionValue'
        self.call = call

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'call': self.call
        })


class function(RuntimeValue):
    def __init__(self, name, parameters: list, declarationEnvironment, body: list, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.type = 'functionValue'
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


class exportValue(RuntimeValue):
    def __init__(self, value, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.type = 'exportValue'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })

class fileValue(RuntimeValue):
    def __init__(self, value:stringValue, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.type = 'fileValue'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })
