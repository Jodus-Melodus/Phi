class RuntimeValue:
    def __init__(self, line: int = -1, column: int = -1) -> None:
        self.line = line
        self.column = column
        self.type = 'runtimeValue'

class NullValue(RuntimeValue):
    def __init__(self) -> None:
        super().__init__()
        self.type = 'nullValue'
        self.value = '_'

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })

class UnknownValue(RuntimeValue):
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

class IntegerValue(RuntimeValue):
    def __init__(self, value, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.type = 'integerValue'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })

class RealValue(RuntimeValue):
    def __init__(self, value, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.type = 'realValue'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })

class StringValue(RuntimeValue):
    def __init__(self, value:str, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        import backend.Methods as bim
        self.type = 'stringValue'
        self.value = value
        self.methods = {
            'length': NativeFunction(lambda args, scope: bim.string_length(self)),
            'format': NativeFunction(lambda args, scope: bim.string_format(args, self))
        }

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })

class BooleanValue(RuntimeValue):
    def __init__(self, value='F') -> None:
        super().__init__()
        self.type = 'booleanValue'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })

class ArrayValue(RuntimeValue):
    def __init__(self, items: dict, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        import backend.Methods as bim
        self.type = 'arrayValue'
        self.items = items
        self.methods = {
            'append': NativeFunction(lambda args, scope: bim.array_append(self, args[0])),
            'length': NativeFunction(lambda args, scope: bim.array_length(self)),
            'join': NativeFunction(lambda args, scope: bim.array_join(self, args[0]))
        }

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'items': self.items,
            'methods': self.methods
        })

class ObjectValue(RuntimeValue):
    def __init__(self, properties: dict, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        import backend.Methods as bim
        self.type = 'objectValue'
        self.properties = properties
        self.methods = {
            'items': NativeFunction(lambda args, scope: bim.object_items(self)),
            'keys': NativeFunction(lambda args, scope: bim.object_keys(self)),
            'update': NativeFunction(lambda args, scope: bim.object_update(self, args[0])),
            'hasAttr': NativeFunction(lambda args, scope: bim.object_has_attribute(self, args[0]))
        }

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'properties': self.properties
        })

class NativeFunction(RuntimeValue):
    def __init__(self, call) -> None:
        super().__init__()
        self.type = 'nativeFunctionValue'
        self.call = call

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'call': self.call
        })


class Function(RuntimeValue):
    def __init__(self, name, parameters: list, declaration_environment, body: list, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.type = 'functionValue'
        self.name = name
        self.parameters = parameters
        self.declaration_environment = declaration_environment
        self.body = body

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'name': self.name,
            'parameters': self.parameters,
            'declarationEnvironment': self.declaration_environment,
            'body': self.body
        })

class ExportValue(RuntimeValue):
    def __init__(self, value, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.type = 'exportValue'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })

class FileValue(RuntimeValue):
    def __init__(self, value:StringValue, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.type = 'fileValue'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'type': self.type,
            'value': self.value
        })