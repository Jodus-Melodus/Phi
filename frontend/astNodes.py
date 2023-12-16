from backend.values import *
from frontend.phi_lexer import *


class Node:
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

# datatypes


class identifierNode(Node):
    def __init__(self, symbol: str, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'identifier'
        self.symbol = symbol

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'symbol': self.symbol
        })


class realLiteralNode(Node):
    def __init__(self, value, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'realLiteral'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })


class integerLiteralNode(Node):
    def __init__(self, value, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'integerLiteral'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })


class stringLiteralNode(Node):
    def __init__(self, value, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'stringLiteral'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })


class nullLiteralNode(Node):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'nullLiteral'
        self.value = 'null'

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })


class objectLiteralNode(Node):
    def __init__(self, properties: list, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'objectLiteral'
        self.properties = properties

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'properties': self.properties
        })


class propertyLiteralNode(Node):
    def __init__(self, key, value, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'propertyLiteral'
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'key': self.key,
            'value': self.value
        })


class arrayLiteralNode(Node):
    def __init__(self, items: list, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'arrayLiteral'
        self.items = items

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'items': self.items
        })


class itemLiteralNode(Node):
    def __init__(self, index, value, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'itemLiteral'
        self.index = index
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'index': self.index,
            'value': self.value
        })


class programNode(Node):
    def __init__(self, body: list = [], line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'program'
        self.body = body

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'body': self.body
        })


class expressionNode(Node):
    def __init__(self, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'expression'

    def __repr__(self) -> str:
        return str({
            'kind': self.kind
        })


class binaryExpressionNode(Node):
    def __init__(self, left, operand: str, right, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
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


# statements
class ifStatementNode(Node):
    def __init__(self, conditionLeft, operand, conditionRight, body, elseBody=[], line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
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


class whileStatementNode(Node):
    def __init__(self, conditionLeft, operand, conditionRight, body, elseBody=[], line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
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


class forStatementNode(Node):
    def __init__(self, declaration, conditionLeft, operand, conditionRight, step, body, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
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
            'declaration': self.declaration,
            'conditionLeft': self.conditionLeft,
            'operand': self.operand,
            'conditionRight': self.conditionRight,
            'body': self.body,
            'step': self.step
        })


class forEachStatementNode(Node):
    def __init__(self, declaration, iterable, body, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'forEachStatement'
        self.declaration = declaration
        self.body = body
        self.iterable = iterable

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'declaration': self.declaration,
            'iterable': self.iterable,
            'body': self.body
        })


class doWhileStatementNode(Node):
    def __init__(self, body, conditionLeft, operand, conditionRight, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
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


class assignmentExpressionNode(Node):
    def __init__(self, assigne, value, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'assignmentExpression'
        self.assigne = assigne
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'assigne': self.assigne,
            'value': self.value
        })


class assignmentBinaryExpressionNode(Node):
    def __init__(self, assigne, operand, value, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
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


class variableDeclarationExpressionNode(Node):
    def __init__(self, datatype: str, identifier: identifierNode, value, constant: bool = False, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
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


class functionDeclarationExpressionNode(Node):
    def __init__(self, name: str, parameters: list = [], body: list = [], line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
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


class memberExpressionNode(Node):
    def __init__(self, object, property, computed: bool, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'memberExpression'
        self.object = object
        self.property = property
        self.computed = computed

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'object': self.object,
            'property': self.property,
            'computed':str(self.computed)
        })


class callExpression(Node):
    def __init__(self, caller, arguments: list, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'callExpression'
        self.caller = caller
        self.arguments = arguments

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'arguments': self.arguments,
            'caller': self.caller
        })


class returnNode(Node):
    def __init__(self, value, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'returnExpression'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })


class exportNode(Node):
    def __init__(self, value, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'exportExpression'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })


class importNode(Node):
    def __init__(self, name, value, line: int, column: int) -> None:
        super().__init__(line, column)
        self.name = name
        self.kind = 'importExpression'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })


class breakNode(Node):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'breakExpression'

    def __repr__(self) -> str:
        return str({
            'kind': self.kind
        })


class continueNode(Node):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'continueExpression'

    def __repr__(self) -> str:
        return str({
            'kind': self.kind
        })


class tryNode(Node):
    def __init__(self, tryBody, exception, exceptBody, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'tryStatement'
        self.tryBody = tryBody
        self.exception = exception
        self.exceptBody = exceptBody

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'tryBody': self.tryBody,
            'exception': self.exception,
            'exceptBody': self.exceptBody
        })


class throwNode(Node):
    def __init__(self, error, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'throwStatement'
        self.error = error

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'error': self.error
        })


class matchNode(Node):
    def __init__(self, value, matches, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'matchStatement'
        self.value = value
        self.matches = matches

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value,
            'matches': self.matches
        })

class caseNode(Node):
    def __init__(self, value, body, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'case'
        self.value = value
        self.body = body

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value,
            'body': self.body
        })