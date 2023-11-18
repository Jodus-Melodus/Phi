

class identifierNode:
    def __init__(self, symbol: str) -> None:
        self.kind = 'identifier'
        self.symbol = symbol

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'symbol': self.symbol
        })


class numericLiteralNode:
    def __init__(self, value) -> None:
        self.kind = 'numericLiteral'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })


class nullLiteralNode:
    def __init__(self) -> None:
        self.kind = 'nullLiteral'
        self.value = 'null'

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })

class programNode:
    def __init__(self, body: list = []) -> None:
        self.kind = 'program'
        self.body = body

    def __repr__(self) -> dict:
        return str({
            'kind': self.kind,
            'body': self.body
        })


class expressionNode:
    def __init__(self) -> None:
        self.kind = 'expression'

    def __repr__(self) -> str:
        return str({
            'kind': self.kind
        })


class binaryExpressionNode:
    def __init__(self, left: expressionNode, operand: str, right: expressionNode) -> None:
        self.kind = 'binaryExpression'
        self.left = left
        self.operand = operand
        self.right = right

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'left': self.left,
            'operand': self.operand,
            'right': self.right
        })


class assignmentExpressionNode:
    def __init__(self, assigne: expressionNode, value: expressionNode) -> None:
        self.kind = 'assignmentExpression'
        self.assigne = assigne
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'assigne': self.assigne,
            'value': self.value
        })


class variableDeclarationExpressionNode:
    def __init__(self, identifier: identifierNode, value: expressionNode, constant:bool=False) -> None:
        self.kind = 'variableDeclarationExpression'
        self.identifier = identifier
        self.value = value
        self.constant = constant

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'identifier': self.identifier,
            'value': self.value,
            'constant':self.constant
        })
    
class functionDeclarationExpressionNode:
    def __init__(self, name:str, parameters:list=[], body:list=[]) -> None:
        self.kind = 'functionDeclaration'
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'name': self.name,
            'parameters': self.parameters,
            'body':self.body
        })    
    
class objectLiteralNode:
    def __init__(self, properties: list) -> None:
        self.kind = 'objectliteral'
        self.properties = properties

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'properties': self.properties
        })


class propertyLiteralNode:
    def __init__(self, key, value) -> None:
        self.kind = 'propertyliteral'
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'key': self.key,
            'value': self.value
        })
    
class memberExpressionNode:
    def __init__(self, object, property, computed:bool) -> None:
        self.kind = 'memberexpression'
        self.object = object
        self.property = property
        self.computed = computed

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'object': self.object,
            'property': self.property
        })

class callExpression:
    def __init__(self, caller:expressionNode, arguements:list) -> None:
        self.kind = 'callexpression'
        self.caller = caller
        self.arguements = arguements

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'arguements': self.arguements,
            'caller': self.caller
        })
