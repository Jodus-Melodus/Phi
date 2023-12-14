from backend.values import *
from frontend.phi_lexer import *


class identifierNode:
    def __init__(self, symbol: str, line: int, column: int) -> None:
        self.kind = 'identifier'
        self.symbol = symbol
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'symbol': self.symbol
        })


class realLiteralNode:
    def __init__(self, value, line: int, column: int) -> None:
        self.kind = 'realLiteral'
        self.value = value
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })


class integerLiteralNode:
    def __init__(self, value, line: int, column: int) -> None:
        self.kind = 'integerLiteral'
        self.value = value
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })


class stringLiteralNode:
    def __init__(self, value, line: int, column: int) -> None:
        self.kind = 'stringLiteral'
        self.value = value
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })


class nullLiteralNode:
    def __init__(self, line: int, column: int) -> None:
        self.kind = 'nullLiteral'
        self.value = 'null'
        self.column = column
        self.line = line

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })


class programNode:
    def __init__(self, body: list = [], line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'program'
        self.body = body

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'body': self.body
        })


class expressionNode:
    def __init__(self, line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'expression'

    def __repr__(self) -> str:
        return str({
            'kind': self.kind
        })


class binaryExpressionNode:
    def __init__(self, left, operand: str, right, line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
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


class ifStatementNode:
    def __init__(self, conditionLeft, operand, conditionRight, body, elseBody=[], line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'ifStatement'
        self.conditionLeft = conditionLeft
        self.operand = operand
        self.conditionRight = conditionRight
        self.body = body
        self.elseBody = elseBody

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'conditionLeft': self.conditionLeft,
            'operand': self.operand,
            'conditionRight': self.conditionRight,
            'body': self.body,
            'elsebody': self.elseBody
        })


class whileStatementNode:
    def __init__(self, conditionLeft, operand, conditionRight, body, elseBody=[], line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'whileStatement'
        self.conditionLeft = conditionLeft
        self.operand = operand
        self.conditionRight = conditionRight
        self.body = body
        self.elseBody = elseBody

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'conditionLeft': self.conditionLeft,
            'operand': self.operand,
            'conditionRight': self.conditionRight,
            'body': self.body,
            'elsebody': self.elseBody
        })
    
class forStatementNode:
    def __init__(self, declaration, conditionLeft, operand, conditionRight, step, body, line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'forStatement'
        self.declaration = declaration
        self.conditionLeft = conditionLeft
        self.operand = operand
        self.conditionRight = conditionRight
        self.body = body
        self.step = step

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'declaration':self.declaration,
            'conditionLeft': self.conditionLeft,
            'operand': self.operand,
            'conditionRight': self.conditionRight,
            'body': self.body,
            'step': self.step
        })


class doWhileStatementNode:
    def __init__(self, body, conditionLeft, operand, conditionRight, line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'doWhileStatement'
        self.body = body
        self.conditionLeft = conditionLeft
        self.operand = operand
        self.conditionRight = conditionRight

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'body': self.body,
            'conditionLeft': self.conditionLeft,
            'operand': self.operand,
            'conditionRight': self.conditionRight
        })


class assignmentExpressionNode:
    def __init__(self, assigne, value, line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'assignmentExpression'
        self.assigne = assigne
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'assigne': self.assigne,
            'value': self.value
        })


class assignmentBinaryExpressionNode:
    def __init__(self, assigne, operand, value, line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'assignmentBinaryExpression'
        self.assigne = assigne
        self.operand = operand
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'assigne': self.assigne,
            'operand': self.operand,
            'value': self.value
        })


class variableDeclarationExpressionNode:
    def __init__(self, datatype:str, identifier:identifierNode, value, constant: bool = False, line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'variableDeclarationExpression'
        self.dataType = datatype
        self.identifier = identifier
        self.value = value
        self.constant = constant

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'datatype': self.dataType,
            'identifier': self.identifier,
            'value': self.value,
            'constant': str(self.constant)
        })


class functionDeclarationExpressionNode:
    def __init__(self, name: str, parameters: list = [], body: list = [], line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'functionDeclaration'
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'name': self.name,
            'parameters': self.parameters,
            'body': self.body
        })


class objectLiteralNode:
    def __init__(self, properties: list, line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'objectLiteral'
        self.properties = properties

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'properties': self.properties
        })


class propertyLiteralNode:
    def __init__(self, key, value, line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'propertyLiteral'
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'key': self.key,
            'value': self.value
        })


class arrayLiteralNode:
    def __init__(self, items: list, line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'arrayLiteral'
        self.items = items

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'items': self.items
        })


class itemLiteralNode:
    def __init__(self, index, value, line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'itemLiteral'
        self.index = index
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'index': self.index,
            'value': self.value
        })


class memberExpressionNode:
    def __init__(self, object, property, computed: bool, line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'memberExpression'
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
    def __init__(self, caller, arguments: list, line:int=-1, column:int=-1) -> None:
        self.line = line
        self.column = column
        self.kind = 'callExpression'
        self.caller = caller
        self.arguments = arguments

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'arguments': self.arguments,
            'caller': self.caller
        })


class returnNode:
    def __init__(self, value, line:int, column:int) -> None:
        self.line = line
        self.column = column
        self.kind = 'returnExpression'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })
    
class exportNode:
    def __init__(self, value, line:int, column:int) -> None:
        self.line = line
        self.column = column
        self.kind = 'exportExpression'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })
    
class importNode:
    def __init__(self, name, value, line:int, column:int) -> None:
        self.name = name
        self.line = line
        self.column = column
        self.kind = 'importExpression'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })
    

class breakNode:
    def __init__(self, line:int, column:int) -> None:
        self.line = line
        self.column = column
        self.kind = 'breakExpression'

    def __repr__(self) -> str:
        return str({
            'kind': self.kind
        })
    
class continueNode:
    def __init__(self, line:int, column:int) -> None:
        self.line = line
        self.column = column
        self.kind = 'continueExpression'

    def __repr__(self) -> str:
        return str({
            'kind': self.kind
        })
