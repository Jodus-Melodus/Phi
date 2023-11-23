from backend.values import *
from frontend.astNodes import *
from frontend.errors import *
from backend.phi_environment import environment, createGlobalEnvironment


class Interpreter:
    def __init__(self) -> None:
        pass

    def evaluateProgram(self, program: programNode, env: environment) -> nullValue|numberValue|objectValue|arrayValue|stringValue|bool|None:
        lastEvaluated = nullValue()

        for statement in program.body:
            lastEvaluated = self.evaluate(statement, env)

        return lastEvaluated

    def evaluateBinaryExpression(self, binaryOperation: binaryExpressionNode, env: environment) -> numberValue|nullValue:
        left = self.evaluate(binaryOperation.left, env)
        right = self.evaluate(binaryOperation.right, env)

        if isinstance(left, numberValue) and isinstance(right, numberValue):
            return self.evaluateNumericBinaryExpression(left, right, binaryOperation.operand, env)
        else:
            return nullValue()
        
    def evaluateNumericBinaryExpression(self, left, right, operand, env: environment) -> numberValue|nullValue:
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
                return nullValue()

    def evaluateIdentifierExpression(self, identifier: identifierNode, env: environment) -> None:
        return env.lookup(identifier.symbol)

    def evaluateAssignmentExpression(self, assignmentExpression: assignmentExpressionNode, env: environment) -> None:
        if isinstance(assignmentExpression.assigne, identifierNode):
            varName = assignmentExpression.assigne.symbol
            return env.assignVariable(varName, self.evaluate(assignmentExpression.value, env))
        elif isinstance(assignmentExpression.assigne, memberExpressionNode):
            member : memberExpressionNode = assignmentExpression.assigne
            varName = member.object.symbol
            prop = member.property.symbol
            currentValue: dict = env.lookup(varName)
            currentValue.properties[prop] = self.evaluate(assignmentExpression.value, env)
            return env.assignVariable(varName, currentValue)
        else:
            syntaxError('Expected an identifier.')

    def evaluateVariableDeclarationExpression(self, declaration: variableDeclarationExpressionNode, env: environment) -> None:
        value = self.evaluate(declaration.value, env)
        return env.declareVariable(declaration.identifier, value, declaration.constant)

    def evaluateFunctionDeclaration(self, declaration: functionDeclarationExpressionNode, env: environment) -> None:
        fn = function(declaration.name, declaration.parameters, env, declaration.body)

        return env.declareVariable(declaration.name, fn)

    def evaluateObjectExpression(self, object: objectLiteralNode, env: environment) -> objectValue:
        properties = {}

        for prop in object.properties:
            a = self.evaluate(prop.value, env)
            properties[prop.key] = a
        obj = objectValue(properties)
        return obj
    
    def evaluateArrayExpression(self, array:arrayLiteralNode, env:environment) -> arrayValue:
        items = {}

        for item in array.items:
            items[item.index] = self.evaluate(item.value, env)
        arr = arrayValue(items)
        return arr

    def evaluateCallExpression(self, callExpr: callExpression, env: environment) -> nullValue|numberValue|objectValue|arrayValue|stringValue|bool|None:
        args = [self.evaluate(x, env) for x in callExpr.arguements]
        fn: nativeFunction|function = self.evaluate(callExpr.caller, env)

        if isinstance(fn, nativeFunction):
            result = fn.call(args, env)
            return result
        elif isinstance(fn, function):
            scope = createGlobalEnvironment(fn.declarationEnvironment)

            if len(fn.parameters) == len(args):
                for i in range(len(fn.parameters)):
                    scope.declareVariable(fn.parameters[i].symbol, args[i])
            elif len(fn.parameters) > len(args):
                syntaxError(f'Too many arguements. Expected {len(fn.parameters)}')
            else:
                syntaxError(f'Too little arguements. Expected {len(fn.parameters)}')

            result = nullValue()
            for statement in fn.body:
                if isinstance(statement, returnNode):
                    return result.value
                result = self.evaluate(statement, scope)
        else:
            syntaxError(f"'{fn}' isn't a function", 0, 0)

    def evaluateMemberExpression(self, member: memberExpressionNode, env: environment) -> None:
        obj = env.lookup(member.object.symbol)

        if isinstance(obj, objectValue):
            if isinstance(member.property, identifierNode):
                if member.property.symbol not in obj.properties:
                    return keyError(member.property.symbol, member.object.symbol)

                if isinstance(member.property, stringValue):
                    return obj.properties[member.property.value]
                return obj.properties[member.property.symbol]
        elif isinstance(obj, arrayValue):
            if isinstance(member.property, numericLiteralNode):
                if member.property.value not in obj.items:
                    return keyError(member.property.value, member.object.symbol)
                
                if isinstance(member.property, numericLiteralNode):
                    return obj.items[member.property.value]
        else:
            return keyError(member.property, member.object.symbol)
    
    def evaluateIfStatement(self, astNode:ifStatementNode, env:environment) -> None:
        left :RuntimeValue = self.evaluate(astNode.conditionLeft, env)
        if not isinstance(astNode.conditionRight, nullValue):
            right :RuntimeValue = self.evaluate(astNode.conditionRight, env)
        else:
            right = nullValue()

        res = False
        if isinstance(right, nullValue):
            if isinstance(left, numberValue):
                if left.value != 0:
                    res = booleanValue('T')
                else:
                    res = booleanValue('F')
            elif isinstance(left, booleanValue):
                res = booleanValue(left.value)
            elif isinstance(left, stringValue):
                res = left.value != ''
        else:
            if isinstance(left, numberValue) and isinstance(right, numberValue):
                match astNode.operand:
                    case '==':
                        res = left.value == right.value
                    case '>':
                        res = left.value > right.value
                    case '<':
                        res = left.value < right.value
                    case '!=':
                        res = left.value != right.value
            elif isinstance(left, booleanValue) and isinstance(right, booleanValue):
                match astNode.operand:
                    case '&':
                        res = left.value and right.value
                    case '|':
                        res = left.value or right.value
                    case '!=':
                        res = left.value != right.value
            elif isinstance(left, stringValue) and isinstance(right, stringValue):
                match astNode.operand:
                    case '==':
                        res = left.value == right.value
                    case '!=':
                        res = left.value != right.value
        if res:
            result = nullValue()
            for statement in astNode.body:
                result = self.evaluate(statement, env)
                if isinstance(statement, returnNode):
                    return result
        return nullValue()
    
    def evaluateWhileStatement(self, astNode:whileStatementNode, env:environment) -> bool:
        while True:
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
                elif isinstance(left, stringValue):
                    res = left.value != ''
            else:
                if isinstance(left, numberValue) and isinstance(right, numberValue):
                    match astNode.operand:
                        case '==':
                            res = left.value == right.value
                        case '>':
                            res = left.value > right.value
                        case '<':
                            res = left.value < right.value
                        case '!=':
                            res = left.value != right.value
                elif isinstance(left, booleanValue) and isinstance(right, booleanValue):
                    match astNode.operand:
                        case '&':
                            res = left.value and right.value
                        case '|':
                            res = left.value or right.value
                        case '!=':
                            res = left.value != right.value
                elif isinstance(left, stringValue) and isinstance(right, stringValue):
                    match astNode.operand:
                        case '==':
                            res = left.value == right.value
                        case '!=':
                            res = left.value != right.value
            if res:
                result = nullValue()
                for statement in astNode.body:
                    if isinstance(statement, returnNode):
                        return result
                    result = self.evaluate(statement, env)
            else:
                break
        return nullValue()

    def evaluateReturnExpression(self, returnExpression:returnNode, env:environment):
        return self.evaluate(returnExpression.value, env)

    def evaluate(self, astNode, env: environment) -> nullValue|numberValue|objectValue|arrayValue|stringValue|bool|None:
        if isinstance(astNode, str):
            return astNode
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
            case 'objectLiteral':
                return self.evaluateObjectExpression(astNode, env)
            case 'callExpression':
                return self.evaluateCallExpression(astNode, env)
            case 'memberExpression':
                return self.evaluateMemberExpression(astNode, env)
            case 'ifStatement':
                return self.evaluateIfStatement(astNode, env)
            case 'whileStatement':
                return self.evaluateWhileStatement(astNode, env)
            case 'arrayLiteral':
                return self.evaluateArrayExpression(astNode, env)
            case 'returnExpression':
                return self.evaluateReturnExpression(astNode, env)

            case 'numericLiteral':
                return numberValue(astNode.value)
            case 'nullLiteral':
                return nullValue()
            case 'stringLiteral':
                return stringValue(astNode.value)
            case _:
                notImplementedError(astNode)
