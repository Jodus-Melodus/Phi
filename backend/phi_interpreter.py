from backend.values import *
from frontend.astNodes import *
from frontend.errors import *
from backend.phi_environment import environment, createGlobalEnvironment
import os

booleanTable = {
    'T': True,
    'F': False
}

dataTypeTable = {
    'int': integerValue,
    'real': realValue,
    'string': stringValue,
    'object': objectValue,
    'array': arrayValue,
    'bool': booleanValue,
    'lambda': function
}
valueTypeTable = {
    'integerValue': ['integerValue', 'realValue'],
    'realValue':['realValue', 'integerValue'],
    'stringValue':['stringValue'],
    'arrayValue':['arrayValue'],
    'nullValue':['nullValue'],
    'booleanValue':['booleanValue'],
    'objectValue':['objectValue'],
    'function':['function'],
}


class Interpreter:
    def __init__(self, filePath:str='') -> None:
        self.filePath = filePath

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

    def evaluateBinaryExpression(self, binaryOperation: binaryExpressionNode, env: environment) -> integerValue | nullValue:
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
            return typeError(self.filePath, self, f"Incompatible types. '{left.type}' and '{right.type}'", right.column, right.line)

    def evaluateArrayAppendBinaryExpression(self, left: arrayValue, right, operand: str) -> arrayValue:
        match operand:
            case '+':
                index = len(left.items)
                left.items[index] = right
                return arrayValue(left.items)
            case _:
                return syntaxError(self.filePath, self, "Cannot preform this operation on arrays.", right.column, right.line)

    def evaluateObjectBinaryExpression(self, left: objectValue, right: objectValue, operand: str) -> objectValue:
        match operand:
            case '+':
                return objectValue(left.properties.update(right.properties))
            case _:
                return syntaxError(self.filePath, self, "Cannot preform this operation on objects.", right.column, right.line)

    def evaluateArrayBinaryExpression(self, left: arrayValue, right: arrayValue, operand: str) -> arrayValue:
        match operand:
            case '+':
                return arrayValue(left.items + right.items)
            case _:
                return syntaxError(self.filePath, self, "Cannot preform this operation on arrays.", right.column, right.line)

    def evaluateStringBinaryExpression(self, left: stringValue, right: stringValue | integerValue | realValue, operand: str) -> stringValue:
        match operand:
            case '+':
                return stringValue(left.value + str(right.value))
            case _:
                return syntaxError(self.filePath, self, "Cannot preform this operation on strings.", right.column, right.line)

    def evaluateNumericBinaryExpression(self, left: integerValue | realValue, right: integerValue | realValue, operand: str) -> realValue:
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
                    return zeroDivisionError(self.filePath, self, right.column, right.line)
            case '^':
                if isinstance(left, realValue) or isinstance(right, realValue):
                    return realValue(left.value ** right.value)
                else:
                    return integerValue(left.value ** right.value)
            case '%':
                if right.value != 0:
                    return integerValue(left.value % right.value)
                else:
                    return zeroDivisionError(self.filePath, self, right.column, right.line)
            case '//':
                if right.value != 0:
                    return integerValue(left.value // right.value)
                else:
                    return zeroDivisionError(self.filePath, self, right.column, right.line)
            case _:
                return syntaxError(self.filePath, self, "Cannot preform this operation on numbers", right.column, right.line)

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
            if value.type in valueTypeTable[value.type]:
                return env.assignVariable(varName, value)
            return typeError(self.filePath, self, f"'{value.type}' is incompatible with '{currentValue.type}'", value.column, value.line)

        elif isinstance(assignmentExpression.assigne, memberExpressionNode):
            member: memberExpressionNode = assignmentExpression.assigne
            varName = member.object
            if assignmentExpression.assigne.computed:
                prop = member.property.symbol
            else:
                prop = self.evaluate(member.property, env)
            currentValue: dict = env.lookup(varName)
            if isinstance(currentValue, error):
                return currentValue
            currentValue.properties[prop] = self.evaluate(assignmentExpression.value, env)
            return env.assignVariable(varName.symbol, currentValue)
        else:
            return syntaxError(self.filePath, self, 'Expected an identifier.', assignmentExpression.assigne.column, assignmentExpression.assigne.line)

    def evaluateVariableDeclarationExpression(self, declaration: variableDeclarationExpressionNode, env: environment) -> None:
        value = self.evaluate(declaration.value, env)
        if isinstance(value, error):
            return value

        if dataTypeTable[declaration.dataType] == type(value):
            return env.declareVariable(declaration.identifier, value, declaration.constant)
        return typeError(self.filePath, self, f"'{value.type}' is incompatible with '{declaration.dataType}'", value.column, value.line)

    def evaluateFunctionDeclaration(self, declaration: functionDeclarationExpressionNode, env: environment) -> None:
        fn = function(declaration.name, declaration.parameters,
                      env, declaration.body)
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
                return syntaxError(self.filePath, self, f'Insufficient arguments provided. Expected {len(fn.parameters)}, but received {len(args)}', column, line)

            result = nullValue()
            for statement in fn.body:
                result = self.evaluate(statement, scope)
                if isinstance(result, error):
                    return result
                if isinstance(statement, returnNode):
                    return result
        else:
            return syntaxError(self.filePath, self, f"'{fn.type}' is not a function", fn.column, fn.line)
        return nullValue()

    def evaluateMemberExpression(self, member: memberExpressionNode, env: environment) -> None:
        if isinstance(member.object, (memberExpressionNode, stringLiteralNode)):
            x = self.evaluate(member.object, env)
        else:
            x = member.object
        
        if not isinstance(x, (objectValue, arrayValue, stringValue)):
            obj: objectValue = env.lookup(x)
        else:
            obj = x


        if isinstance(obj, objectValue):
            if isinstance(member.property, identifierNode):
                if isinstance(list(obj.properties.keys())[0], stringValue):
                    old = obj.properties.copy()
                    new = {}
                    for key in old:
                        if isinstance(key, stringValue):
                            new[key.value] = old[key]
                    obj.properties = new

                if member.property.symbol in obj.methods:
                    return obj.methods[member.property.symbol]
                elif member.property.symbol in obj.properties:
                    return obj.properties[member.property.symbol]
                else:
                    v = self.evaluate(member.property, env)
                    if isinstance(v, error):
                        return v
                    elif v.value in obj.properties:
                        return obj.properties[v.value]
                    else:
                        return keyError(self.filePath, self, v, obj, v.column, v.line)

            elif isinstance(member.property, stringLiteralNode):
                return obj.properties[member.property.value]
            else:
                return typeError(self.filePath, self, f"Expected an identifier or a string value got {member.property}", self.column, self.line)
        elif isinstance(obj, (arrayValue, stringValue)):
            if isinstance(member.property, integerLiteralNode):
                if member.property.value not in obj.items:
                    return keyError(self.filePath, self, member.property.value, member.object.symbol, member.property.column, member.property.line)

                elif isinstance(member.property, integerLiteralNode):
                    return obj.items[member.property.value]
            elif isinstance(member.property, identifierNode):
                if member.property.symbol in obj.methods:
                    return obj.methods[member.property.symbol]
                else:
                    value = self.evaluate(member.property, env)
                    if isinstance(value, error):
                        return value
                    value = value.value
                    if value in obj.items:
                        return obj.items[value]
                    else:
                        return syntaxError(self.filePath, self, f"'{member.property.symbol}' is not a valid method or property.", member.column, member.line)
            else:
                return syntaxError(self.filePath, self, f"'{member.property.symbol}' is not valid.", member.column, member.line)
        else:
            return keyError(self.filePath, self, member.property.symbol, member.object.symbol, member.property.column, member.property.line)

    def evaluateIfStatement(self, ifStatement: ifStatementNode, env: environment) -> None:
        left: RuntimeValue = self.evaluate(ifStatement.conditionLeft, env)
        if isinstance(left, error):
            return left
        if not isinstance(ifStatement.conditionRight, nullValue):
            right: RuntimeValue = self.evaluate(
                ifStatement.conditionRight, env)
            if isinstance(right, error):
                return right
        else:
            right = nullValue()

        res = False
        res = self.checkCondition(left, ifStatement.operand, right)
        if res:
            result = nullValue()
            for statement in ifStatement.body:
                if isinstance(statement, (continueNode, breakNode)):
                    return statement
                result = self.evaluate(statement, env)
                if isinstance(result, (error, returnNode)):
                    return result
        else:
            if ifStatement.elseBody != []:
                result = nullValue()
                for statement in ifStatement.elseBody:
                    if isinstance(statement, (continueNode, breakNode)):
                        return statement
                    result = self.evaluate(statement, env)
                    if isinstance(result, (error, returnNode)):
                        return result
        return nullValue()

    def evaluateWhileStatement(self, whileStatement: whileStatementNode, env: environment) -> bool:
        while True:
            left: RuntimeValue = self.evaluate(
                whileStatement.conditionLeft, env)
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
                    if isinstance(statement, (error, returnNode, breakNode)):
                        return result
                    if isinstance(result, continueNode):
                        break
                    result = self.evaluate(statement, env)
                    if isinstance(result, (error, breakNode)):
                        return result
                    if isinstance(result, continueNode):
                        break
            else:
                if whileStatement.elseBody != []:
                    result = nullValue()
                    for statement in whileStatement.elseBody:
                        if isinstance(result, (error, returnNode, breakNode)):
                            return result
                        if isinstance(result, continueNode):
                            break
                        result = self.evaluate(statement, env)
                        if isinstance(result, (error, breakNode)):
                            return result
                        if isinstance(result, continueNode):
                            break
                break
        return nullValue()

    def evaluateForStatement(self, forLoop: forStatementNode, env: environment) -> None:
        self.evaluateVariableDeclarationExpression(forLoop.declaration, env)

        while True:
            left: RuntimeValue = self.evaluate(forLoop.conditionLeft, env)
            if isinstance(left, error):
                return left
            if not isinstance(forLoop.conditionRight, nullValue):
                right: RuntimeValue = self.evaluate(
                    forLoop.conditionRight, env)
                if isinstance(right, error):
                    return right
            else:
                right = nullValue()

            res = False
            res = self.checkCondition(left, forLoop.operand, right)
            if res:
                result = nullValue()
                for statement in forLoop.body:
                    if isinstance(statement, (error, returnNode, breakNode)):
                        return result
                    result = self.evaluate(statement, env)
                    if isinstance(result, (error, breakNode)):
                        return result
                    if isinstance(result, continueNode):
                        break
                result = self.evaluateAssignmentBinaryExpression(
                    forLoop.step, env)
            else:
                break
        return nullValue()

    def evaluateForEachStatement(self, forEachLoop: forEachStatementNode, env: environment) -> None:
        self.evaluateVariableDeclarationExpression(
            forEachLoop.declaration, env)

        array = self.evaluate(forEachLoop.iterable, env)

        for item in array.items:
            assignmentExpr = assignmentExpressionNode(identifierNode(
                forEachLoop.declaration.identifier, forEachLoop.declaration.line, forEachLoop.declaration.column), integerLiteralNode(array.items[item].value, -1, -1))
            res = self.evaluateAssignmentExpression(assignmentExpr, env)
            if isinstance(res, error):
                return res

            result = nullValue()
            for statement in forEachLoop.body:
                if isinstance(statement, (error, returnNode, breakNode)):
                    return result
                result = self.evaluate(statement, env)
                if isinstance(result, (error, breakNode)):
                    return result
                if isinstance(result, continueNode):
                    break

        return nullValue()

    def evaluateDoWhileStatement(self, doWhile: doWhileStatementNode, env: environment) -> None:
        res = True
        while True:
            if res:
                result = nullValue()
                for statement in doWhile.body:
                    if isinstance(statement, (returnNode, error, breakNode)):
                        return result
                    if isinstance(statement, continueNode):
                        break
                    result = self.evaluate(statement, env)
                    if isinstance(result, (error, breakNode)):
                        return result
                    if isinstance(result, continueNode):
                        break

                left: RuntimeValue = self.evaluate(doWhile.conditionLeft, env)
                if isinstance(left, error):
                    return result
                if not isinstance(doWhile.conditionRight, nullValue):
                    right: RuntimeValue = self.evaluate(
                        doWhile.conditionRight, env)
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
            currentValue = integerLiteralNode(
                currValue.value, expr.column, expr.line)
        elif isinstance(currValue, realValue):
            currentValue = realLiteralNode(
                currValue.value, expr.column, expr.line)
        elif isinstance(currValue, stringValue):
            currentValue = stringLiteralNode(currValue.value, expr.column, expr.line)
        else:
            return typeError(self.filePath, self, f"Incompatible type '{currValue}'", expr.column, expr.line)
        

        binexpr = binaryExpressionNode(
            currentValue, expr.operand[0], expr.value, expr.line, expr.column)
        newValue = self.evaluateBinaryExpression(binexpr, env)

        if isinstance(newValue, error):
            return newValue
        elif isinstance(newValue, realValue):
            v = realLiteralNode(newValue.value, expr.line, expr.column)
        elif isinstance(newValue, integerValue):
            v = integerLiteralNode(newValue.value, expr.line, expr.column)
        elif isinstance(newValue, stringValue):
            v = stringLiteralNode(newValue.value, expr.column, expr.line)
        else:
            return typeError(self.filePath, self, f"Incompatible types. '{currentValue}' and '{newValue}'", expr.column, expr.line)

        return self.evaluateAssignmentExpression(assignmentExpressionNode(expr.assigne, v), env)

    def evaluateExportExpression(self, exportExpression: exportNode, env: environment):
        return exportValue(self.evaluate(exportExpression.value, env), exportExpression.line, exportExpression.column)

    def evaluateImportExpression(self, importExpression: importNode, env: environment):
        from shell import run

        result = nullValue()
        for i in range(len(importExpression.values)):
            path = importExpression.values[i]

            if isinstance(path, identifierNode):
                path = path.symbol
            elif isinstance(path, stringValue):
                path = path.value
            else:
                return syntaxError(self.filePath, self, "Expected an identifier or a stringValue", importExpression.column, importExpression.line)

            name = importExpression.names[i].symbol

            path = path.lower()
            path = f'Modules/{path}.phi'
            if os.path.exists(path):
                with open(path, 'r') as f:
                    code = '\n'.join(f.readlines())

                code = run(code, path)
                if isinstance(code, exportValue):
                    if name.isupper():
                        result = env.declareVariable(name, code.value, True)
                    else:
                        result = env.declareVariable(name, code.value, False)
                else:
                    result = nullValue()
            else:
                return fileNotFoundError(self.filePath, self, f'{path}', importExpression.column, importExpression.line)
        return result

    def evaluateTryStatement(self, tryStatement: tryNode, env: environment) -> None:
        result = nullValue()
        for statement in tryStatement.tryBody:
            if isinstance(statement, (returnNode, error, breakNode)):
                break
            if isinstance(statement, continueNode):
                break
            result = self.evaluate(statement, env)
            if isinstance(result, (error, breakNode)):
                break
            if isinstance(result, continueNode):
                break

        if isinstance(result, error):
            if result.type == tryStatement.exception.symbol:
                result = nullValue()
                for statement in tryStatement.exceptBody:
                    if isinstance(statement, (error, breakNode)):
                        return statement
                    if isinstance(statement, continueNode):
                        break
                    result = self.evaluate(statement, env)
                    if isinstance(result, (error, breakNode)):
                        return result
                    if isinstance(result, continueNode):
                        break
            else:
                return result
        else:
            return result

    def evaluateThrowStatement(self, throwStmt: throwNode, env: environment) -> None:
        match throwStmt.error.symbol:
            case 'syntaxError':
                return syntaxError(self.filePath, '', '', throwStmt.column, throwStmt.line)
            case 'zeroDivisionError':
                return zeroDivisionError(self.filePath, '', throwStmt.column, throwStmt.line)
            case 'typeError':
                return typeError(self.filePath, '', '', throwStmt.column, throwStmt.line)
            case 'keyError':
                return keyError(self.filePath, '', '', '', throwStmt.column, throwStmt.line)
            case 'notImplementedError':
                return notImplementedError(self.filePath, '', '', throwStmt.column, throwStmt.line)
            case 'invalidCharacterError':
                return invalidCharacterError(self.filePath, '', '', throwStmt.column, throwStmt.line)
            case 'nameError':
                return nameError(self.filePath, '', '', throwStmt.column, throwStmt.line)

    def evaluateMatchStatement(self, matchStmt: matchNode, env: environment) -> None:
        value = self.evaluate(matchStmt.value, env)

        for match in matchStmt.matches:
            v = self.evaluate(match.value, env)
            if value.value == v.value:
                result = nullValue()
                for statement in match.body:
                    if isinstance(statement, (error, breakNode)):
                        return statement
                    if isinstance(statement, continueNode):
                        break
                    result = self.evaluate(statement, env)
                    if isinstance(result, (error, breakNode, returnNode)):
                        return result
                    if isinstance(result, continueNode):
                        break
                return result
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
            case 'forEachStatement':
                return self.evaluateForEachStatement(astNode, env)
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
            case 'tryStatement':
                return self.evaluateTryStatement(astNode, env)
            case 'throwStatement':
                return self.evaluateThrowStatement(astNode, env)
            case 'matchStatement':
                return self.evaluateMatchStatement(astNode, env)

            case 'integerLiteral':
                return integerValue(astNode.value, astNode.line, astNode.column)
            case 'realLiteral':
                return realValue(astNode.value, astNode.line, astNode.column)
            case 'stringLiteral':
                return stringValue(astNode.value, astNode.line, astNode.column)
            case 'nullLiteral':
                return nullValue()
            case _:
                return notImplementedError(self.filePath, self, astNode.kind, astNode.column, astNode.line)
