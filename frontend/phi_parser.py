from frontend.phi_lexer import Lexer, Token, TT
from frontend.astNodes import *
from frontend.errors import *

# prescidence orders
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

    def eat(self) -> Token:
        return self.tokens.pop(0)

    def get(self) -> Token:
        return self.tokens[0]

    def genAST(self) -> None:
        while self.get().type != TT.eof:
            statement = self.parseStatement()
            if statement:
                self.program.body.append(statement)

        return self.program

    def parseStatement(self) -> None:
        match self.get().type:
            case TT.var:
                return self.parseVariableDeclaration()
            case TT.const:
                return self.parseVariableDeclaration()
            case TT.fn:
                return self.parseFunctionDeclaration()
            case TT._if:
                return self.parseIfStatement()
            case TT._while:
                return self.parseWhileStatement()
            case _:
                return self.parseExpression()

    def parseExpression(self) -> None:
        return self.parseAssignmentExpression()
    
    def parseWhileStatement(self) -> None:
        self.eat()

        operand = ''
        if self.get().type == TT.openParenthesis:
            self.eat()
            conditionLeft = self.parseExpression()
            if self.get().type in (TT.equal, TT.greaterThan, TT.lessThan, TT._and, TT._or):
                operand = self.eat().value
                conditionRight = self.parseExpression()
            else:
                conditionRight = nullValue()

            if self.get().type == TT.closeParenthesis:
                self.eat()
                if self.get().type == TT.openBrace:
                    self.eat()
                    body = []
                    while self.get().type != TT.closeBrace:
                        statement = self.parseStatement()
                        if statement:
                            body.append(statement)
                        if self.get().type == TT.eof:
                            syntaxError("Expected a '}'", self.get().column, self.get().line)
                    self.eat()
                else:
                    syntaxError("Expected a '{'", self.get().column, self.get().line)
        else:
            syntaxError("Expected a '('", self.get().column, self.get().line)
        return whileStatementNode(conditionLeft, operand, conditionRight, body)
    
    def parseIfStatement(self) -> None:
        self.eat()

        operand = ''
        if self.get().type == TT.openParenthesis:
            self.eat()
            conditionLeft = self.parseExpression()
            if self.get().type in (TT.equal, TT.greaterThan, TT.lessThan, TT._and, TT._or):
                operand = self.eat().value
                conditionRight = self.parseExpression()
            else:
                conditionRight = nullValue()

            if self.get().type == TT.closeParenthesis:
                self.eat()
                if self.get().type == TT.openBrace:
                    self.eat()
                    body = []
                    while self.get().type != TT.closeBrace:
                        statement = self.parseStatement()
                        if statement:
                            body.append(statement)
                        if self.get().type == TT.eof:
                            syntaxError("Expected a '}'", self.get().column, self.get().line)
                    self.eat()
                else:
                    syntaxError("Expected a '{'", self.get().column, self.get().line)
        else:
            syntaxError("Expected a '('", self.get().column, self.get().line)
        return ifStatementNode(conditionLeft, operand, conditionRight, body)
    
    def parseFunctionDeclaration(self) -> None:
        self.eat()
        name = self.eat().value
        
        args = self.parseArguements()
        parameters = []
        for parameter in args:
            if parameter.kind == 'identifier':
                parameters.append(parameter)
            else:
                syntaxError("Expected parameters to be of string type.", self.get().column, self.get().line)

        if self.get().type == TT.openBrace:
            self.eat()
        else:
            syntaxError("Expected a '{'", self.get().column, self.get().line)

        body = []
        while self.get().type != TT.closeBrace:
            statement = self.parseStatement()
            if statement:
                body.append(statement)
            if self.get().type == TT.eof:
                syntaxError("Expected a '}'", self.get().column, self.get().line)

        self.eat()

        return functionDeclarationExpressionNode(name, parameters, body)

    def parseVariableDeclaration(self) -> None:
        if self.get().type == TT.var:
            self.eat()
            identifier = self.eat().value
            if (self.get().type == TT.eof) or (self.get().type == TT.lineend):
                self.eat()
                return variableDeclarationExpressionNode(identifier, nullLiteralNode())
            else:
                self.eat()
                return variableDeclarationExpressionNode(identifier, self.parseExpression())
        elif self.get().type == TT.const:
            self.eat()
            identifier = self.eat().value
            if (self.get().type == TT.eof) or (self.get().type == TT.lineend):
                self.eat()
                return variableDeclarationExpressionNode(identifier, nullLiteralNode(), True)
            else:
                self.eat()
                return variableDeclarationExpressionNode(identifier, self.parseExpression(), True)

    def parseAssignmentExpression(self) -> None:
        left = self.parseObjectExpression()

        if self.get().type == TT.assignmentOperator:
            self.eat()
            value = self.parseAssignmentExpression()
            return assignmentExpressionNode(left, value)
        else:
            return left

    def parseObjectExpression(self) -> None:
        if self.get().type != TT.openBrace:
            return self.parseAdditiveExpression()
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
                    value = self.parseExpression()
                    properties.append(propertyLiteralNode(key, value))
                    if self.get().type in (TT.comma, TT.lineend):
                        self.eat()
                    elif self.get().type == TT.closeBrace:
                        break
                    else:
                        syntaxError("Expected a ',' or a '}'", self.get().column, self.get().line)
                else:
                    syntaxError("Expected a value", self.get().column, self.get().line)
            else:
                syntaxError('Something went wrong', self.get().column, self.get().line)
        self.eat()
        return objectLiteralNode(properties)

    def parseAdditiveExpression(self) -> None:
        left = self.parseMultiplicativeExpression()

        while self.get().value in ['+', '-',]:
            operand = self.eat().value
            right = self.parseMultiplicativeExpression()
            left = binaryExpressionNode(left, operand, right)

        return left

    def parseMultiplicativeExpression(self) -> None:
        left = self.parseCallMemberExpression()

        while self.get().value in ['*', '/', '^', '%']:
            operand = self.eat().value
            right = self.parseCallMemberExpression()
            left = binaryExpressionNode(left, operand, right)

        return left

    def parseCallMemberExpression(self) -> None:
        member = self.parseMemberExpression()

        if self.get().type == TT.openParenthesis:
            return self.parseCallExpression(member)

        return member

    def parseCallExpression(self, caller) -> None:
        callExpr = callExpression(caller, self.parseArguements())

        if self.get().type == TT.openParenthesis:
            callExpr = self.parseCallExpression(callExpr)

        return callExpr

    def parseArguements(self) -> None:
        if self.get().type == TT.openParenthesis:
            self.eat()
            if self.get().type == TT.closeParenthesis:
                self.eat()
                args = []
                return []
            else:
                args = self.parseArguementsList()
        if self.get().type == TT.closeParenthesis:
            self.eat()
        else:
            syntaxError("Expected a ')'", self.get().column, self.get().line)

        return args

    def parseArguementsList(self) -> None:
        args = [self.parseAssignmentExpression()]

        while (self.get().type == TT.comma):
            self.eat()
            args.append(self.parseAssignmentExpression())

        return args

    def parseMemberExpression(self) -> None:
        obj = self.parsePrimaryExpression()

        while (self.get().type == TT.period) or (self.get().type == TT.openBracket):
            operand = self.eat()

            if operand.type == TT.period:
                computed = False
                prop = self.parsePrimaryExpression()
                if prop.kind != ('identifier'):
                    syntaxError("invalid syntax", self.get().column, self.get().line)
            else:
                computed = True
                prop = self.parseExpression()
                if self.get().type != TT.closeBracket:
                    syntaxError("Expected ']'", self.get().column, self.get().line)
                else:
                    self.eat()

            obj = memberExpressionNode(obj, prop, computed)
        return obj

    def parsePrimaryExpression(self) -> None:
        match self.get().type:
            case TT.int | TT.real:
                return numericLiteralNode(float(self.eat().value))
            case TT.string:
                return stringLiteralNode(self.eat().value)
            case TT.identifier:
                return identifierNode(self.eat().value)
            case TT.openParenthesis:
                self.eat()  # open paren
                value = self.parseExpression()
                self.eat()  # close paren
                return value
            case TT.lineend:
                self.eat()
