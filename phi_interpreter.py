from values import *
from astNodes import *
from errors import *
from environment_ import environment


class interpreter:
    def __init__(self) -> None:
        pass

    def evaluateProgram(self, program: programNode, env: environment) -> None:
        lastEvaluated = nullValue()

        for statement in program.body:
            lastEvaluated = self.evaluate(statement, env)

        return lastEvaluated

    def evaluateBinaryExpression(self, binaryOperation: binaryExpressionNode, env: environment) -> numberValue | nullValue:
        left = self.evaluate(binaryOperation.left, env)
        right = self.evaluate(binaryOperation.right, env)

        if isinstance(left, numberValue) and isinstance(right, numberValue):
            return self.evaluateNumericBinaryExpression(left, right, binaryOperation.operand, env)
        else:
            return nullValue
        
    def evaluateNumericBinaryExpression(self, left, right, operand, env: environment) -> numberValue | nullValue:
        match operand:
            case '+':
                return numberValue(left.value + right.value)
            case '-':
                return numberValue(left.value - right.value)
            case '*':
                return numberValue(left.value * right.value)
            case '/':
                return numberValue(left.value / right.value)
            case '^':
                return numberValue(left.value ** right.value)
            case '%':
                return numberValue(left.value % right.value)
            case _:
                return nullValue

    def evaluateIdentifierExpression(self, identifier: identifierNode, env: environment) -> None:
        return env.lookup(identifier.symbol)

    def evaluateAssignmentExpression(self, assignmentExpression: assignmentExpressionNode, env: environment) -> None:
        if isinstance(assignmentExpression.assigne, identifierNode):
            varName = assignmentExpression.assigne.symbol
            return env.assignVariable(varName, self.evaluate(assignmentExpression.value, env))
        elif isinstance(assignmentExpression.assigne, memberExpressionNode):
            member: memberExpressionNode = assignmentExpression.assigne
            varName = member.object.symbol
            prop = member.property.symbol
            currentValue: dict = env.lookup(varName)
            currentValue.properties[prop] = assignmentExpression.value
            return env.assignVariable(varName, currentValue)
        else:
            syntaxError('Expected an identifier.')

    def evaluateVariableDeclarationExpression(self, declaration: variableDeclarationExpressionNode, env: environment) -> None:
        return env.declareVariable(declaration.identifier, self.evaluate(declaration.value, env), declaration.constant)

    def evaluateFunctionDeclaration(self, declaration: functionDeclarationExpressionNode, env: environment) -> None:
        fn = function(declaration.name, declaration.parameters,
                      env, declaration.body)

        return env.declareVariable(declaration.name, fn)

    def evaluateObjectExpression(self, obj: objectLiteralNode, env: environment) -> None:
        properties = {}

        for prop in obj.properties:
            a = self.evaluate(prop.value, env)
            properties[prop.key] = a
        obj = objectValue(properties)
        return obj

    def evaluateCallExpression(self, callExpr: callExpression, env: environment) -> None:
        args = [self.evaluate(x, env) for x in callExpr.arguements]
        fn: nativeFunction = self.evaluate(callExpr.caller, env)

        if fn.type == 'nativeFunctionValue':
            result = fn.call(args, env)
            return result
        elif fn.type == 'FunctionValue':
            func: function = fn
            scope = environment(func.declarationEnvironment)

            if len(func.parameters) == len(args):
                for i in range(len(func.parameters)):
                    scope.declareVariable(func.parameters[i].symbol, args[i])
            else:
                syntaxError("Too many or little arguements.")

            result = nullValue()
            for statement in func.body:
                result = self.evaluate(statement, scope)
            return result
        else:
            syntaxError(f"'{fn}' isn't a function", 0, 0)

    def evaluateMemberExpression(self, member: memberExpressionNode, env: environment) -> None:
        obj: objectValue = env.lookup(member.object.symbol)

        if isinstance(member.property, identifierNode):
            if member.property.symbol not in obj.properties:
                keyError(member.property.symbol, member.object.symbol)

            return obj.properties[member.property.symbol]
        else:
            keyError(keyError(member.property.symbol, member.object.symbol))
    
    def evaluateIfStatement(self, astNode:ifStatementNode, env:environment):
        left :RuntimeValue = self.evaluate(astNode.conditionLeft, env)
        if not isinstance(astNode.conditionRight, nullValue):
            right :RuntimeValue = self.evaluate(astNode.conditionRight, env)
        else:
            right = nullValue()

        res = False
        if isinstance(right, nullValue):
            if isinstance(left, numberValue):
                if left.value != 0:
                    res = booleanValue(True)
                else:
                    res = booleanValue(False)
            elif isinstance(left, booleanValue):
                res = booleanValue(left.value)
        else:
            if isinstance(left, numberValue) and isinstance(right, numberValue):
                res = nullValue
                match astNode.operand:
                    case '==':
                        res = left.value == right.value
                    case '>':
                        res = left.value > right.value
                    case '<':
                        res = left.value < right.value
            elif isinstance(left, booleanValue) and isinstance(right, booleanValue):
                res = nullValue
                match astNode.operand:
                    case '&':
                        res = left.value and right.value
                    case '|':
                        res = left.value or right.value

        if res:
            for statement in astNode.body:
                res = self.evaluate(statement, env)
        return res

    def evaluate(self, astNode, env: environment) -> None:
        match astNode.kind:
            case 'program':
                return self.evaluateProgram(astNode, env)
            case 'binaryExpression':
                return self.evaluateBinaryExpression(astNode, env)
            case 'identifier':
                return self.evaluateIdentifierExpression(astNode, env)
            case 'assignmentExpression':
                return self.evaluateAssignmentExpression(astNode, env)
            case 'variableDeclarationExpression':
                return self.evaluateVariableDeclarationExpression(astNode, env)
            case 'functionDeclaration':
                return self.evaluateFunctionDeclaration(astNode, env)
            case 'objectliteral':
                return self.evaluateObjectExpression(astNode, env)
            case 'callexpression':
                return self.evaluateCallExpression(astNode, env)
            case 'memberexpression':
                return self.evaluateMemberExpression(astNode, env)
            case 'ifstatement':
                return self.evaluateIfStatement(astNode, env)

            case 'numericLiteral':
                return numberValue(astNode.value)
            case 'nullLiteral':
                return nullValue
            case 'stringLiteral':
                return stringValue(astNode.value)
            case _:
                notImplementedError(astNode)
