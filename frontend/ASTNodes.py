from backend.RuntimeValue import *
from frontend.Lexer import *

class ASTNode:
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

# datatypes
class IdentifierNode(ASTNode):
    def __init__(self, symbol: str, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'identifier'
        self.symbol = symbol

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'symbol': self.symbol
        })

class RealLiteralNode(ASTNode):
    def __init__(self, value, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'realLiteral'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })
    
class UnknownLiteralNode(ASTNode):
    def __init__(self, value, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'unknownLiteral'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })

class IntegerLiteralNode(ASTNode):
    def __init__(self, value, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'integerLiteral'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })

class StringLiteralNode(ASTNode):
    def __init__(self, value, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'stringLiteral'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })

class NullLiteralNode(ASTNode):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'nullLiteral'
        self.value = 'null'

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })

class ObjectLiteralNode(ASTNode):
    def __init__(self, properties: list, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'objectLiteral'
        self.properties = properties

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'properties': self.properties
        })

class PropertyLiteralNode(ASTNode):
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

class ArrayLiteralNode(ASTNode):
    def __init__(self, items: list, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'arrayLiteral'
        self.items = items

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'items': self.items
        })

class ItemLiteralNode(ASTNode):
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

class ProgramNode(ASTNode):
    def __init__(self, body: list = None, line: int = -1, column: int = -1) -> None:
        if body is None:
            body = []
        super().__init__(line, column)
        self.kind = 'program'
        self.body = body

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'body': self.body
        })

class ExpressionNode(ASTNode):
    def __init__(self, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'expression'

    def __repr__(self) -> str:
        return str({
            'kind': self.kind
        })

class BinaryExpressionNode(ASTNode):
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
class IfStatementNode(ASTNode):
    def __init__(self, left_condition, operand, right_condition, body, else_body=None, line: int = -1, column: int = -1) -> None:
        if else_body is None:
            else_body = []
        super().__init__(line, column)
        self.kind = 'ifStatement'
        self.left_condition = left_condition
        self.operand = operand
        self.right_condition = right_condition
        self.body = body
        self.else_body = else_body

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'left_condition': self.left_condition,
            'operand': self.operand,
            'right_condition': self.right_condition,
            'body': self.body,
            'else_body': self.else_body
        })


class WhileStatementNode(ASTNode):
    def __init__(self, left_condition, operand, right_condition, body, else_body=None, line: int = -1, column: int = -1) -> None:
        if else_body is None:
            else_body = []
        super().__init__(line, column)
        self.kind = 'whileStatement'
        self.left_condition = left_condition
        self.operand = operand
        self.right_condition = right_condition
        self.body = body
        self.else_body = else_body

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'left_condition': self.left_condition,
            'operand': self.operand,
            'right_condition': self.right_condition,
            'body': self.body,
            'else_body': self.else_body
        })

class ForStatementNode(ASTNode):
    def __init__(self, declaration, left_condition, operand, right_condition, step, body, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'forStatement'
        self.declaration = declaration
        self.left_condition = left_condition
        self.operand = operand
        self.right_condition = right_condition
        self.body = body
        self.step = step

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'declaration': self.declaration,
            'left_condition': self.left_condition,
            'operand': self.operand,
            'right_condition': self.right_condition,
            'body': self.body,
            'step': self.step
        })

class ForEachStatementNode(ASTNode):
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

class DoWhileStatementNode(ASTNode):
    def __init__(self, body, left_condition, operand, right_condition, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.kind = 'doWhileStatement'
        self.body = body
        self.left_condition = left_condition
        self.operand = operand
        self.right_condition = right_condition

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'body': self.body,
            'left_condition': self.left_condition,
            'operand': self.operand,
            'right_condition': self.right_condition
        })

class AssignmentExpressionNode(ASTNode):
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

class AssignmentBinaryExpressionNode(ASTNode):
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

class VariableDeclarationExpressionNode(ASTNode):
    def __init__(self, datatype: str, identifier: IdentifierNode, value, constant: bool = False, line: int = -1, column: int = -1) -> None:
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

class FunctionDeclarationExpressionNode(ASTNode):
    def __init__(self, name: str, parameters: list = None, body: list = None, line: int = -1, column: int = -1) -> None:
        if parameters is None:
            parameters = []
        if body is None:
            body = []
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

class MemberExpressionNode(ASTNode):
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

class CallExpression(ASTNode):
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

class ReturnNode(ASTNode):
    def __init__(self, value, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'returnExpression'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })

class ExportNode(ASTNode):
    def __init__(self, value, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'exportExpression'
        self.value = value

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'value': self.value
        })

class ImportNode(ASTNode):
    def __init__(self, names, values:list, line: int, column: int) -> None:
        super().__init__(line, column)
        self.names = names
        self.kind = 'importExpression'
        self.values = values

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'names':self.names,
            'values': self.values
        })

class BreakNode(ASTNode):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'breakExpression'

    def __repr__(self) -> str:
        return str({
            'kind': self.kind
        })

class ContinueNode(ASTNode):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'continueExpression'

    def __repr__(self) -> str:
        return str({
            'kind': self.kind
        })

class TryNode(ASTNode):
    def __init__(self, try_body, exception, except_body, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'tryStatement'
        self.try_body = try_body
        self.exception = exception
        self.except_body = except_body

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'try_body': self.try_body,
            'exception': self.exception,
            'except_body': self.except_body
        })

class ThrowNode(ASTNode):
    def __init__(self, error, message:str, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'throwStatement'
        self.error = error
        self.msg = message

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'error': self.error,
            'msg':self.msg
        })

class MatchNode(ASTNode):
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

class CaseNode(ASTNode):
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
    
class DeleteNode(ASTNode):
    def __init__(self, variable, line: int, column: int) -> None:
        super().__init__(line, column)
        self.kind = 'delete'
        self.variable = variable

    def __repr__(self) -> str:
        return str({
            'kind': self.kind,
            'variable': self.variable
        })