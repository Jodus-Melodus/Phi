from backend.values import *
from frontend.astNodes import *
from frontend.errors import *
from backend.phi_environment import environment, createGlobalEnvironment

booleanTable = {
    'T':True,
    'F':False
}

dataTypeTable = {
    'int':integerValue,
    'real':realValue,
    'string':stringValue,
    'object':objectValue,
    'array':arrayValue,
    'bool':booleanValue,
    'lambda':function
}

class Interpreter:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return 'Interpreter'

    def checkCondition(self, left: RuntimeValue, operand: str, right: RuntimeValue) -> bool:
        res = False
        if isinstance(right, nullValue):
            if isinstance(left, (realValue, integerValue)):
                if left.value != 0:
                    res = booleanValue('T')
                else:
                    res = booleanValue('F')
            elif isinstance(left, booleanValue):
                res = True if left.value == 'T' else False
            elif isinstance(left, stringValue):
                res = left.value != ''
        else:
            if isinstance(left, (realValue, integerValue)) and isinstance(right, (realValue, integerValue)):
                match operand:
                    case '==':
                        res = left.value == right.value
                    case '>':
                        res = left.value > right.value
                    case '<':
                        res = left.value < right.value
                    case '>=':
                        res = left.value >= right.value
                    case '<=':
                        res = left.value <= right.value
                    case '!=':
                        res = left.value != right.value
            elif isinstance(left, booleanValue) and isinstance(right, booleanValue):
                match operand:
                    case '&':
                        res = booleanTable[left.value] and booleanTable[right.value]
                    case '|':
                        res = booleanTable[left.value] or booleanTable[right.value]
                    case '!=':
                        res = booleanTable[left.value] != booleanTable[right.value]
            elif isinstance(left, stringValue) and isinstance(right, stringValue):
                match operand:
                    case '==':
                        res = left.value == right.value
                    case '!=':
                        res = left.value != right.value
        return res

    def evaluateProgram(self, program: programNode, env: environment) -> nullValue | integerValue | objectValue | arrayValue | stringValue | bool | None:
        lastEvaluated = nullValue()

        for statement in program.body:
            lastEvaluated = self.evaluate(statement, env)
            if isinstance(lastEvaluated, error):
                return lastEvaluated

        return lastEvaluated

    def evaluateBinaryExpression(self, binaryOperation:binaryExpressionNode, env: environment) -> integerValue | nullValue:
        left = self.evaluate(binaryOperation.left, env)
        if isinstance(left, error):
            return left
        right = self.evaluate(binaryOperation.right, env)
        if isinstance(right, error):
            return right

        if isinstance(left, (realValue, integerValue)) and isinstance(right, (realValue, integerValue)):
            return self.evaluateNumericBinaryExpression(left, right, binaryOperation.operand)
        elif isinstance(left, stringValue) and isinstance(right, (stringValue, (realValue, integerValue))):
            return self.evaluateStringBinaryExpression(left, right, binaryOperation.operand)
        
        elif isinstance(left, arrayValue):
            return self.evaluateArrayAppendBinaryExpression(left, right, binaryOperation.operand)
        else:
            return syntaxError(self, "Cannot preform this operation.", right.column, right.line)
        
    def evaluateArrayAppendBinaryExpression(self, left:arrayValue, right, operand:str) -> arrayValue:
        match operand:
            case '+':
                index = len(left.items)
                left.items[index] = right
                return arrayValue(left.items)
            case _:
                return syntaxError(self, "Cannot preform this operation on arrays.", right.column, right.line)
        
    def evaluateObjectBinaryExpression(self, left:objectValue, right:objectValue, operand:str) -> objectValue:
        match operand:
            case '+':
                return objectValue(left.properties.update(right.properties))
            case _:
                return syntaxError(self, "Cannot preform this operation on objects.", right.column, right.line)

    def evaluateArrayBinaryExpression(self, left:arrayValue, right:arrayValue, operand:str) -> arrayValue:
        match operand:
            case '+':
                return arrayValue(left.items + right.items)
            case _:
                return syntaxError(self, "Cannot preform this operation on arrays.", right.column, right.line)

    def evaluateStringBinaryExpression(self, left:stringValue, right:stringValue|integerValue|realValue, operand:str) -> stringValue:
        match operand:
            case '+':
                return stringValue(left.value + right.value)
            case _:
                return syntaxError(self, "Cannot preform this operation on strings.", right.column, right.line)

    def evaluateNumericBinaryExpression(self, left:integerValue|realValue, right:integerValue|realValue, operand:str) -> realValue:
        match operand:
            case '+':
                if isinstance(left, realValue) or isinstance(right, realValue):
                    return realValue(left.value + right.value)
                else:
                    return integerValue(left.value + right.value)
            case '-':
                if isinstance(left, realValue) or isinstance(right, realValue):
                    return realValue(left.value - right.value)
                else:
                    return integerValue(left.value - right.value)
            case '*':
                if isinstance(left, realValue) or isinstance(right, realValue):
                    return realValue(left.value * right.value)
                else:
                    return integerValue(left.value * right.value)
            case '/':
                if right.value != 0:
                    return realValue(left.value / right.value)
                else:
                    return zeroDivisionError(self, right.column, right.line)
            case '^':
                if isinstance(left, realValue) or isinstance(right, realValue):
                    return realValue(left.value ** right.value)
                else:
                    return integerValue(left.value ** right.value)
            case '%':
                if right.value != 0:
                    return integerValue(left.value % right.value)
                else:
                    return zeroDivisionError(self, right.column, right.line)
            case '//':
                if right.value != 0:
                    return integerValue(left.value // right.value)
                else:
                    return zeroDivisionError(self, right.column, right.line)
            case _:
                return syntaxError(self, "Cannot preform this operation on numbers", right.column, right.line)

# --------------------------------------------------------------------------------------------------------------------------------

    def evaluateIdentifierExpression(self, identifier: identifierNode, env: environment) -> None:
        return env.lookup(identifier)

    def evaluateAssignmentExpression(self, assignmentExpression: assignmentExpressionNode, env: environment) -> None:
        if isinstance(assignmentExpression.assigne, identifierNode):
            varName = assignmentExpression.assigne.symbol
            currentValue = env.lookup(assignmentExpression.assigne)
            if isinstance(currentValue, error):
                return currentValue
            value = self.evaluate(assignmentExpression.value, env)
            if isinstance(value, error):
                return value
            if value.type == currentValue.type:
                return env.assignVariable(varName, value)
            return syntaxError(self, f"'{value.type}' is incompatible with '{currentValue.type}'", value.column, value.line)
        
        elif isinstance(assignmentExpression.assigne, memberExpressionNode):
            member: memberExpressionNode = assignmentExpression.assigne
            varName = member.object
            prop = member.property.symbol
            currentValue: dict = env.lookup(varName)
            currentValue.properties[prop] = self.evaluate(
                assignmentExpression.value, env)
            return env.assignVariable(varName, currentValue)
        else:
            return syntaxError(self, 'Expected an identifier.', assignmentExpression.assigne.column, assignmentExpression.assigne.line)

    def evaluateVariableDeclarationExpression(self, declaration: variableDeclarationExpressionNode, env: environment) -> None:
        value = self.evaluate(declaration.value, env)
        if isinstance(value, error):
            return value
        
        if dataTypeTable[declaration.dataType] == type(value):
            return env.declareVariable(declaration.identifier, value, declaration.constant)
        return syntaxError(self, f"'{value.type}' is incompatible with '{declaration.dataType}'", value.column, value.line)

    def evaluateFunctionDeclaration(self, declaration: functionDeclarationExpressionNode, env: environment) -> None:
        fn = function(declaration.name, declaration.parameters, env, declaration.body)
        return env.declareVariable(declaration.name, fn)

    def evaluateObjectExpression(self, object: objectLiteralNode, env: environment) -> objectValue:
        properties = {}

        for prop in object.properties:
            a = self.evaluate(prop.value, env)
            if isinstance(a, error):
                return a
            properties[prop.key] = a
        obj = objectValue(properties, object.line, object.column)
        return obj

    def evaluateArrayExpression(self, array: arrayLiteralNode, env: environment) -> arrayValue:
        items = {}

        for item in array.items:
            items[item.index] = self.evaluate(item.value, env)
        arr = arrayValue(items, array.line, array.column)
        return arr

    def evaluateCallExpression(self, callExpr: callExpression, env: environment) -> nullValue | integerValue | objectValue | arrayValue | stringValue | bool | None:
        args = []
        for arg in callExpr.arguments:
            a = self.evaluate(arg, env)
            if isinstance(a, error):
                return a
            args.append(a)
        fn: nativeFunction | function = self.evaluate(callExpr.caller, env)
        if isinstance(fn, error):
            return fn

        if isinstance(fn, nativeFunction):
            result = fn.call(args, env)
            return result
        elif isinstance(fn, function):
            scope = createGlobalEnvironment(fn.declarationEnvironment)
            for variable in env.variables:
                scope.declareVariable(variable, env.variables[variable])

            if len(fn.parameters) == len(args):
                for i in range(len(fn.parameters)):
                    scope.declareVariable(fn.parameters[i].symbol, args[i])
            else:
                if len(fn.parameters) > 0:
                    column = fn.parameters[-1].column
                    line = fn.parameters[-1].line
                else:
                    column = fn.column
                    line = fn.line
                return syntaxError(self, f'Insufficient arguments provided. Expected {len(fn.parameters)}, but received {len(args)}', column, line)

            result = nullValue()
            for statement in fn.body:
                result = self.evaluate(statement, scope)
                if isinstance(result, error):
                    return result
                if isinstance(statement, returnNode):
                    return result
        else:
            return syntaxError(self, f"'{fn.type}' is not a function", fn.column, fn.line)

    def evaluateMemberExpression(self, member: memberExpressionNode, env: environment) -> None:
        obj:objectValue = env.lookup(member.object)

        if isinstance(obj, objectValue):
            if isinstance(member.property, identifierNode):
                if member.property.symbol in obj.methods:
                    return obj.methods[member.property.symbol]
                elif member.property.symbol not in obj.properties:
                    return keyError(self, member.property.symbol, member.object.symbol, member.property.column, member.property.line)

                elif isinstance(member.property, stringValue):
                    return obj.properties[member.property.value]
                return obj.properties[member.property.symbol]
        elif isinstance(obj, (arrayValue, stringValue)):
            if isinstance(member.property, integerLiteralNode):
                if member.property.value not in obj.items:
                    return keyError(self, member.property.value, member.object.symbol, member.property.column, member.property.line)

                elif isinstance(member.property, integerLiteralNode):
                    return obj.items[member.property.value]
            elif isinstance(member.property, identifierNode):
                if member.property.symbol in obj.methods:
                    return obj.methods[member.property.symbol]
                else:
                    value = self.evaluate(member.property, env).value
                    if value in obj.items:
                        return obj.items[value]
                    else:
                        return syntaxError(self, f"'{member.property.symbol}' is not a valid method or property.", member.column, member.line)
            else:
                return syntaxError(self, f"'{member.property.symbol}' is not valid.", member.column, member.line)
        else:
            return keyError(self, member.property, member.object.symbol, member.property.column, member.property.line)

    def evaluateIfStatement(self, ifStatement: ifStatementNode, env: environment) -> None:
        left: RuntimeValue = self.evaluate(ifStatement.conditionLeft, env)
        if isinstance(left, error):
            return left
        if not isinstance(ifStatement.conditionRight, nullValue):
            right: RuntimeValue = self.evaluate(ifStatement.conditionRight, env)
            if isinstance(right, error):
                return right
        else:
            right = nullValue()

        res = False
        res = self.checkCondition(left, ifStatement.operand, right)
        if res:
            result = nullValue()
            for statement in ifStatement.body:
                result = self.evaluate(statement, env)
                if isinstance(result, (error, returnNode)):
                    return result
        else:
            if ifStatement.elseBody != []:
                result = nullValue()
                for statement in ifStatement.elseBody:
                    result = self.evaluate(statement, env)
                    if isinstance(result, (error, returnNode)):
                        return result
        return nullValue()

    def evaluateWhileStatement(self, whileStatement: whileStatementNode, env: environment) -> bool:
        while True:
            left: RuntimeValue = self.evaluate(whileStatement.conditionLeft, env)
            if isinstance(left, error):
                return left
            if not isinstance(whileStatement.conditionRight, nullValue):
                right: RuntimeValue = self.evaluate(
                    whileStatement.conditionRight, env)
                if isinstance(right, error):
                    return right
            else:
                right = nullValue()

            res = False
            res = self.checkCondition(left, whileStatement.operand, right)
            if res:
                result = nullValue()
                for statement in whileStatement.body:
                    if isinstance(statement, (error, returnNode, breakNode, continueNode)):
                        return result
                    result = self.evaluate(statement, env)
                    if isinstance(result, error):
                        return result
            else:
                if whileStatement.elseBody != []:
                    result = nullValue()
                    for statement in whileStatement.elseBody:
                        if isinstance(result, (error, returnNode, breakNode, continueNode)):
                            return result
                        result = self.evaluate(statement, env)
                        if isinstance(result, error):
                            return result
                break
        return nullValue()
    
    def evaluateForStatement(self, forLoop:forStatementNode, env:environment) -> None:
        self.evaluateVariableDeclarationExpression(forLoop.declaration, env)

        while True:
            left: RuntimeValue = self.evaluate(forLoop.conditionLeft, env)
            if isinstance(left, error):
                return left
            if not isinstance(forLoop.conditionRight, nullValue):
                right: RuntimeValue = self.evaluate(forLoop.conditionRight, env)
                if isinstance(right, error):
                    return right
            else:
                right = nullValue()

            res = False
            res = self.checkCondition(left, forLoop.operand, right)
            if res:
                result = nullValue()
                for statement in forLoop.body:
                    if isinstance(statement, (error, returnNode, breakNode, continueNode)):
                        return result
                    result = self.evaluate(statement, env)
                    if isinstance(result, error):
                        return result
                result = self.evaluateAssignmentBinaryExpression(forLoop.step, env)
                if isinstance(result, error):
                    return result
            else:
                break
        return nullValue()


    def evaluateDoWhileStatement(self, doWhile: doWhileStatementNode, env: environment) -> None:
        res = True
        while True:
            if res:
                result = nullValue()
                for statement in doWhile.body:
                    if isinstance(statement, (returnNode, error, breakNode, continueNode)):
                        return result
                    result = self.evaluate(statement, env)
                    if isinstance(result, error):
                        return result

                left: RuntimeValue = self.evaluate(doWhile.conditionLeft, env)
                if isinstance(left, error):
                    return result
                if not isinstance(doWhile.conditionRight, nullValue):
                    right: RuntimeValue = self.evaluate(doWhile.conditionRight, env)
                    if isinstance(right, error):
                        return result
                else:
                    right = nullValue()

                res = self.checkCondition(left, doWhile.operand, right)
            else:
                break
        return nullValue()

    def evaluateReturnExpression(self, returnExpression: returnNode, env: environment):
        return self.evaluate(returnExpression.value, env)

    def evaluateAssignmentBinaryExpression(self, expr: assignmentBinaryExpressionNode, env: environment) -> None:
        currValue = env.lookup(expr.assigne)
        if isinstance(currValue, integerValue):
            currentValue = integerLiteralNode(currValue.value, expr.column, expr.line)
        elif isinstance(currValue, realValue):
            currentValue = realLiteralNode(currValue.value, expr.column, expr.line)

        binexpr = binaryExpressionNode(currentValue, expr.operand[0], expr.value, expr.line, expr.column)
        newValue = self.evaluateBinaryExpression(binexpr, env)

        if isinstance(newValue, error):
            return newValue
        elif isinstance(newValue, realValue):
            v = realLiteralNode(newValue.value, expr.line, expr.column)
        elif isinstance(newValue, integerValue):
            v = integerLiteralNode(newValue.value, expr.line, expr.column)

        return self.evaluateAssignmentExpression(assignmentExpressionNode(expr.assigne, v), env)

    def evaluateExportExpression(self, exportExpression: exportNode, env: environment):
        return exportValue(self.evaluate(exportExpression.value, env), exportExpression.line, exportExpression.column)

    def evaluateImportExpression(self, importExpression:importNode, env:environment):
        from main import run
        path = importExpression.value
        if isinstance(path, identifierNode):
            path = path.symbol

            if isinstance(importExpression.name, nullValue):
                name = path
            elif isinstance(importExpression.name, identifierNode):
                name = importExpression.name.symbol

            with open(f'{path}.phi', 'r') as f:
                code = '\n'.join(f.readlines())

            code = run(code)
            if isinstance(code, exportValue):
                return env.declareVariable(name, code.value, True)
            else:
                return nullValue()

    def evaluate(self, astNode, env: environment) -> nullValue | integerValue | objectValue | arrayValue | stringValue | None:
        if isinstance(astNode, (str, float, int, error)):
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
            case 'forStatement':
                return self.evaluateForStatement(astNode, env)
            case 'doWhileStatement':
                return self.evaluateDoWhileStatement(astNode, env)
            case 'arrayLiteral':
                return self.evaluateArrayExpression(astNode, env)
            case 'returnExpression':
                return self.evaluateReturnExpression(astNode, env)
            case 'assignmentBinaryExpression':
                return self.evaluateAssignmentBinaryExpression(astNode, env)
            case 'exportExpression':
                return self.evaluateExportExpression(astNode, env)
            case 'importExpression':
                return self.evaluateImportExpression(astNode, env)

            case 'integerLiteral':
                return integerValue(astNode.value, astNode.line, astNode.column)
            case 'realLiteral':
                return realValue(astNode.value, astNode.line, astNode.column)
            case 'stringLiteral':
                return stringValue(astNode.value, astNode.line, astNode.column)
            case 'nullLiteral':
                return nullValue()
            case _:
                return notImplementedError(self, astNode.kind, astNode.column, astNode.line)
