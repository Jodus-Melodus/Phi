from frontend.phi_lexer import Token, TT
from frontend.astNodes import *
from frontend.errors import *

# Prescidence orders
# assignment
# object
# additive
# multiplicative
# call
# member
# primary

class Parser:
    def __init__(self, tokens: list) -> None:
        self.tokens = tokens
        self.program = programNode([])
        self.conditionalOperators = (TT.equal, TT.notequal, TT.greaterThan,
                                     TT.lessThan, TT.greaterThanEqual, TT.lessThanEqual, TT._and, TT._or)
        self.column = 0
        self.line = 0

    def __str__(self) -> str:
        return 'Parser'

    def eat(self) -> Token:
        self.column = self.tokens[0].column
        self.line = self.tokens[0].line
        return self.tokens.pop(0)

    def get(self) -> Token:
        return self.tokens[0]

    def genAST(self) -> programNode:
        while self.get().type != TT.eof:
            if self.get().type == TT.lineend:
                self.eat()
                continue
            else:
                statement = self.parseStatement()
                if isinstance(statement, error):
                    return statement
                if statement:
                    self.program.body.append(statement)

        return self.program

    def parseStatement(self) -> None:
        match self.get().type:
            case TT.lineend:
                self.eat()
            case TT.int:
                return self.parseVariableDeclaration()
            case TT.real:
                return self.parseVariableDeclaration()
            case TT.string:
                return self.parseVariableDeclaration()
            case TT.array:
                return self.parseVariableDeclaration()
            case TT.obj:
                return self.parseVariableDeclaration()
            case TT._lambda:
                return self.parseVariableDeclaration()
            case TT.bool:
                return self.parseVariableDeclaration()
            case TT.fn:
                return self.parseFunctionDeclaration()
            case TT._if:
                return self.parseIfStatement()
            case TT._while:
                return self.parseWhileStatement()
            case TT.do:
                return self.parseDoWhileStatement()
            case _:
                return self.parseExpression()

    def parseExpression(self) -> None:
        return self.parseAssignmentExpression()

    def parseDoWhileStatement(self) -> None:
        self.eat()

        operand = ''
        if self.get().type == TT.openBrace:
            self.eat()
            body = []
            while self.get().type != TT.closeBrace:
                statement = self.parseStatement()
                if isinstance(statement, error):
                    return statement
                if statement:
                    body.append(statement)
                if self.get().type == TT.eof:
                    return syntaxError(self, "Expected a '}'", self.column, self.line)
            self.eat()
            if self.get().type == TT._while:
                self.eat()
                if self.get().type == TT.openParenthesis:
                    self.eat()
                    conditionLeft = self.parseExpression()
                    if isinstance(conditionLeft, error):
                        return conditionLeft
                    if self.get().type in self.conditionalOperators:
                        operand = self.eat().value
                        conditionRight = self.parseExpression()
                        if isinstance(conditionRight, error):
                            return conditionRight
                    else:
                        conditionRight = nullValue()
                    if self.get().type == TT.closeParenthesis:
                        self.eat()
                    else:
                        return syntaxError(self, "Expected a ')'", self.column, self.line)
                else:
                    return syntaxError(self, "Expected a '('", self.column, self.line)
            else:
                return syntaxError(self, "Expected a 'while'", self.column, self.line)
        else:
            return syntaxError(self, "Expected a '{'", self.column, self.line)

        return doWhileStatementNode(body, conditionLeft, operand, conditionRight, self.line, self.column)

    def parseWhileStatement(self) -> None:
        self.eat()

        operand = ''
        if self.get().type == TT.openParenthesis:
            self.eat()
            conditionLeft = self.parseExpression()
            if isinstance(conditionLeft, error):
                return conditionLeft
            if self.get().type in self.conditionalOperators:
                operand = self.eat().value
                conditionRight = self.parseExpression()
                if isinstance(conditionRight, error):
                    return conditionRight
            else:
                conditionRight = nullValue()

            if self.get().type == TT.closeParenthesis:
                self.eat()
                if self.get().type == TT.openBrace:
                    self.eat()
                    body = []
                    while self.get().type != TT.closeBrace:
                        statement = self.parseStatement()
                        if isinstance(statement, error):
                            return statement
                        if statement:
                            body.append(statement)
                        if self.get().type == TT.eof:
                            return syntaxError(self, "Expected a '}'", self.column, self.line)
                    self.eat()
                    if self.get().type == TT._else:
                        self.eat()
                        if self.get().type == TT.openBrace:
                            self.eat()
                            elseBody = []
                            while self.get().type != TT.closeBrace:
                                statement = self.parseStatement()
                                if isinstance(statement, error):
                                    return statement
                                if statement:
                                    elseBody.append(statement)
                                if self.get().type == TT.eof:
                                    return syntaxError(self, "Expected a '}'", self.column, self.line)
                            self.eat()
                        else:
                            return syntaxError(self, "Expected a '{'", self.column, self.line)
                    else:
                        return whileStatementNode(conditionLeft, operand, conditionRight, body)
                else:
                    return syntaxError(self, "Expected a '{'", self.column, self.line)
        else:
            return syntaxError(self, "Expected a '('", self.column, self.line)
        return whileStatementNode(conditionLeft, operand, conditionRight, body, elseBody, self.line, self.column)

    def parseIfStatement(self) -> None:
        self.eat()

        operand = ''
        if self.get().type == TT.openParenthesis:
            self.eat()
            conditionLeft = self.parseExpression()
            if isinstance(conditionLeft, error):
                return conditionLeft
            if self.get().type in self.conditionalOperators:
                operand = self.eat().value
                conditionRight = self.parseExpression()
                if isinstance(conditionRight, error):
                    return conditionRight
            else:
                conditionRight = nullValue()

            if self.get().type == TT.closeParenthesis:
                self.eat()
                if self.get().type == TT.openBrace:
                    self.eat()
                    body = []
                    while self.get().type != TT.closeBrace:
                        statement = self.parseStatement()
                        if isinstance(statement, error):
                            return statement
                        if statement:
                            body.append(statement)
                        if self.get().type == TT.eof:
                            return syntaxError(self, "Expected a '}'", self.column, self.line)
                    self.eat()
                    if self.get().type == TT._else:
                        self.eat()
                        if self.get().type == TT.openBrace:
                            self.eat()
                            elseBody = []
                            while self.get().type != TT.closeBrace:
                                statement = self.parseStatement()
                                if isinstance(statement, error):
                                    return statement
                                if statement:
                                    elseBody.append(statement)
                                if self.get().type == TT.eof:
                                    return syntaxError(self, "Expected a '}'", self.column, self.line)
                            self.eat()
                        else:
                            return syntaxError(self, "Expected a '{'", self.column, self.line)
                    else:
                        return ifStatementNode(conditionLeft, operand, conditionRight, body)
                else:
                    return syntaxError(self, "Expected a '{'", self.column, self.line)
        else:
            return syntaxError(self, "Expected a '('", self.column, self.line)
        return ifStatementNode(conditionLeft, operand, conditionRight, body, elseBody, self.line, self.column)

    def parseFunctionDeclaration(self) -> None:
        self.eat()
        if self.get().type in (TT.identifier, TT.anonymous):
            name = self.eat().value
        else:
            return syntaxError(self, 'Expected a name', self.column, self.line)

        args = self.parseArguments()
        if isinstance(args, error):
            return args
        parameters = []
        for parameter in args:
            if parameter.kind == 'identifier':
                parameters.append(parameter)
            else:
                return syntaxError(self, "Expected parameters to be of string type.", self.column, self.line)

        if self.get().type == TT.openBrace:
            self.eat()
        else:
            return syntaxError(self, "Expected a '{'", self.column, self.line)

        body = []
        while self.get().type != TT.closeBrace:
            statement = self.parseStatement()
            if isinstance(statement, error):
                return statement
            if statement:
                body.append(statement)
            if self.get().type == TT.eof:
                return syntaxError(self, "Expected a '}'", self.column, self.line)

        self.eat()

        return functionDeclarationExpressionNode(str(name), parameters, body, self.line, self.column)

    def parseVariableDeclaration(self) -> None:
        datatype = self.eat().type
        identifier = self.eat().value
        if identifier.isupper():
            constant = True
        else:
            constant = False
        if (self.get().type == TT.eof) or (self.get().type == TT.lineend):
            self.eat()
            return variableDeclarationExpressionNode(datatype, identifier, nullLiteralNode(self.line, self.column), constant, self.line, self.column)
        else:
            self.eat()
            statement = self.parseStatement()
            if isinstance(statement, error):
                return statement
            return variableDeclarationExpressionNode(datatype, identifier, statement, constant, self.line, self.column)

    def parseAssignmentExpression(self) -> None:
        left = self.parseObjectExpression()
        if isinstance(left, error):
            return left

        if self.get().type == TT.assignmentOperator:
            self.eat()
            value = self.parseStatement()
            if isinstance(value, error):
                return value
            return assignmentExpressionNode(left, value)
        elif self.get().type == TT.assignmentBinaryOperation:
            operand = self.eat().value
            value = self.parsePrimaryExpression()
            if isinstance(value, error):
                return value
            return assignmentBinaryExpressionNode(left, operand, value, self.line, self.column)
        else:
            return left

    def parseObjectExpression(self) -> None:
        if self.get().type != TT.openBrace:
            value = self.parseArrayExpression()
            if isinstance(value, error):
                return value
            return value
        else:
            self.eat()

        properties = []

        while self.get().type != TT.eof:
            if self.get().type == TT.closeBrace:
                break
            elif self.get().type == TT.lineend:
                self.eat()
                continue
            elif self.get().type == TT.identifier:
                key = self.eat().value
                if self.get().type == TT.colon:
                    self.eat()
                    value = self.parseStatement()
                    if isinstance(value, error):
                        return value
                    properties.append(propertyLiteralNode(key, value))
                    if self.get().type in (TT.comma, TT.lineend):
                        self.eat()
                    elif self.get().type == TT.closeBrace:
                        break
                    else:
                        return syntaxError(self, "Expected a ',' or a '}'", self.column, self.line)
                else:
                    return syntaxError(self, "Expected a value", self.column, self.line)
            else:
                return syntaxError(self, 'Something went wrong', self.column, self.line)
        self.eat()
        return objectLiteralNode(properties, self.line, self.column)

    def parseArrayExpression(self) -> None:
        if self.get().type != TT.openBracket:
            value = self.parseAdditiveExpression()
            if isinstance(value, error):
                return value
            return value
        else:
            self.eat()

        items = []
        index = -1

        while self.get().type != TT.eof:
            if self.get().type == TT.closeBracket:
                break
            elif self.get().type == TT.lineend:
                self.eat()
                continue
            else:
                index += 1
                value = self.parseExpression()
                if isinstance(value, error):
                    return value
                items.append(itemLiteralNode(index, value))
                if self.get().type in (TT.comma, TT.lineend):
                    self.eat()
                elif self.get().type == TT.closeBracket:
                    break
                else:
                    return syntaxError(self, "Expected a ',' or a ']'", self.column, self.line)
        self.eat()
        return arrayLiteralNode(items, self.line, self.column)

    def parseAdditiveExpression(self) -> None:
        left = self.parseMultiplicativeExpression()
        if isinstance(left, error):
            return left

        while self.get().value in ['+', '-',]:
            operand = self.eat().value
            right = self.parseMultiplicativeExpression()
            if isinstance(right, error):
                return right
            left = binaryExpressionNode(left, str(operand), right, self.line, self.column)

        return left

    def parseMultiplicativeExpression(self) -> None:
        left = self.parseCallMemberExpression()
        if isinstance(left, error):
            return left

        while self.get().value in ['*', '/', '^', '%', '//']:
            operand = self.eat().value
            right = self.parseCallMemberExpression()
            if isinstance(right, error):
                return right
            left = binaryExpressionNode(left, str(operand), right, self.line, self.column)

        return left

    def parseCallMemberExpression(self) -> None:
        member = self.parseMemberExpression()
        if isinstance(member, error):
            return member

        if self.get().type == TT.openParenthesis:
            value = self.parseCallExpression(member)
            if isinstance(value, error):
                return value
            return value

        return member

    def parseCallExpression(self, caller) -> None:
        value = self.parseArguments()
        if isinstance(value, error):
            return value
        callExpr = callExpression(caller, value, self.line, self.column)

        if self.get().type == TT.openParenthesis:
            callExpr = self.parseCallExpression(callExpr)
            if isinstance(callExpr, error):
                return callExpr

        return callExpr

    def parseArguments(self) -> None:
        if self.get().type == TT.openParenthesis:
            self.eat()
            if self.get().type == TT.closeParenthesis:
                self.eat()
                args = []
                return []
            else:
                args = self.parseArgumentsList()
                if isinstance(args, error):
                    return args
        if self.get().type == TT.closeParenthesis:
            self.eat()
        else:
            return syntaxError(self, "Expected a ')'", self.column, self.line)

        return args

    def parseArgumentsList(self) -> None:
        args = [self.parseAssignmentExpression()]
        if isinstance(args[0], error):
            return args[0]

        while (self.get().type == TT.comma):
            self.eat()
            value = self.parseAssignmentExpression()
            if isinstance(value, error):
                return value
            args.append(value)

        return args

    def parseMemberExpression(self) -> None:
        obj = self.parsePrimaryExpression()
        if isinstance(obj, error):
            return obj

        while (self.get().type == TT.period) or (self.get().type == TT.openBracket):
            operand = self.eat()

            if operand.type == TT.period:
                computed = False
                prop = self.parsePrimaryExpression()
                if isinstance(prop, error):
                    return prop
                if prop.kind != ('identifier'):
                    return syntaxError(self, "Invalid syntax", self.column, self.line)
            else:
                computed = True
                prop = self.parseExpression()
                if isinstance(prop, error):
                    return prop
                if self.get().type != TT.closeBracket:
                    return syntaxError(self, "Expected a ']'", self.column, self.line)
                else:
                    self.eat()

            obj = memberExpressionNode(obj, prop, computed, self.line, self.column)
        return obj

    def parsePrimaryExpression(self) -> None:
        match self.get().type:
            case TT.intValue:
                return integerLiteralNode(int(self.eat().value), self.line, self.column)
            case TT.realValue:
                return realLiteralNode(float(self.eat().value), self.line, self.column)
            case TT.stringValue:
                return stringLiteralNode(self.eat().value, self.line, self.column)
            case TT.identifier:
                return identifierNode(str(self.eat().value), self.line, self.column)
            case TT.openParenthesis:
                self.eat()
                value = self.parseExpression()
                if isinstance(value, error):
                    return value
                self.eat()
                return value
            case TT.lineend:
                self.eat()
            case TT._return:
                self.eat()
                value = self.parseStatement()
                if isinstance(value, error):
                    return value
                return returnNode(value, self.line, self.column)
            case TT.export:
                self.eat()
                value = self.parseStatement()
                if isinstance(value, error):
                    return value
                return exportNode(value, self.line, self.column)
            case TT._import:
                self.eat()
                if self.get().type == TT.identifier:
                    value = self.parseStatement()
                    if isinstance(value, error):
                        return value
                    
                    if self.get().type == TT._as:
                        self.eat()
                        name = self.parsePrimaryExpression()
                        return importNode(name, value, self.line, self.column)
                    else:
                        return importNode(nullValue(), value, self.line, self.column)
                else:
                    return syntaxError(self, "Expected an identifier", self.column, self.line)
            case _:
                return syntaxError(self, 'Invalid token found', self.column, self.line)
