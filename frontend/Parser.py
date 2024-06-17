from frontend.Lexer import Token, TT
from frontend.ASTNodes import *
from frontend.Error import *

class Parser:
    def __init__(self, tokens: list, filePath:str="") -> None:
        self.file_path = filePath
        self.tokens = tokens
        self.program = ProgramNode([])
        self.conditional_operators = (TT.equal, TT.not_equal, TT.greater_than, TT.less_than, TT.greater_than_equal, TT.less_than_equal, TT._and, TT._or)
        self.column = 0
        self.line = 0

        self.datatypeMap = {
            "int":IntegerLiteralNode(0, self.line, self.column),
            "real":RealLiteralNode(0.0, self.line, self.column),
            "string":StringLiteralNode("", self.line, self.column),
            "array":ArrayLiteralNode([], self.line, self.column),
            "object":ObjectLiteralNode([], self.line, self.column),
            "bool":IdentifierNode('F', self.line, self.column),
            "lambda":NullLiteralNode(self.line, self.column),
            "unknown":NullLiteralNode(self.line, self.column)
        }

    def eat(self) -> Token:
        self.column = self.tokens[0].column
        self.line = self.tokens[0].line
        return self.tokens.pop(0)

    def get(self) -> Token:
        if len(self.tokens) == 0:
            return Token(TT.eof, "", self.column, self.line)
        
        return self.tokens[0]

    def generate_AST(self) -> ProgramNode | list[Error]:
        errors = []

        while len(self.tokens) > 0 and self.get().type != TT.eof:
            if self.get().type == TT.lineend:
                self.eat()
            else:
                statement = self.parse_statement()
                if isinstance(statement, Error):
                    errors.append(statement)
                elif isinstance(statement, ASTNode):
                    self.program.body.append(statement)

        return errors or self.program

    def parse_statement(self) -> None:
        match self.get().type:
            case TT.lineend:
                self.eat()
            case TT.int:
                return self.parse_variable_declaration()
            case TT.real:
                return self.parse_variable_declaration()
            case TT.string:
                return self.parse_variable_declaration()
            case TT.array:
                return self.parse_variable_declaration()
            case TT.obj:
                return self.parse_variable_declaration()
            case TT._lambda:
                return self.parse_variable_declaration()
            case TT.bool:
                return self.parse_variable_declaration()
            case TT.fn:
                return self.parse_function_declaration()
            case TT.unknown:
                return self.parse_variable_declaration()
            case TT._if:
                return self.parse_if_statement()
            case TT._while:
                return self.parse_while_statement()
            case TT._for:
                return self.parse_for_statement()
            case TT.do:
                return self.parse_do_while_statement()
            case TT._try:
                return self.parse_try_statement()
            case TT.throw:
                return self.parse_throw_statement()
            case TT._match:
                return self.parse_match_statement()
            case TT._del:
                return self.parse_delete_statement()
            case _:
                return self.parse_expression()

    def parse_expression(self) -> None:
        return self.parse_assignment_expression()

    def parse_delete_statement(self) -> None:
        self.eat()
        if self.get().type != TT.identifier:
            return SyntaxError(self.file_path, self, "Expected an identifier", self.column, self.line)
        v = self.eat().value
        return DeleteNode(v, self.line, self.column)
    
    def parse_match_statement(self) -> None:
        self.eat()

        if self.get().type != TT.identifier:
            return SyntaxError(self.file_path, self, "Expected an identifier", self.column, self.line)
        value = self.parse_primary_expression()
        if isinstance(value, Error):
            return value
        if self.get().type != TT.open_brace:
            return SyntaxError(self.file_path, self, "Expected a '{'", self.column, self.line)
        self.eat()
        matches = []
        while self.get().type != TT.close_brace:
            if self.get().type == TT._case:
                statement = self.parse_case_statement()
                if isinstance(statement, Error):
                    return statement
                if statement:
                    matches.append(statement)
                if self.get().type == TT.eof:
                    return SyntaxError(self.file_path, self, "Expected a '}'", self.column, self.line)
            elif self.get().type in (TT.lineend):
                self.eat()
            else:
                return SyntaxError(self.file_path, self, "Expected 'case'", self.column, self.line)
        self.eat()
        return MatchNode(value, matches, self.line, self.column)
    
    def parse_case_statement(self) -> None:
        self.eat()

        if self.get().type not in (TT.int_value, TT.real_value, TT.string_value):
            return SyntaxError(self.file_path, self, "Expected a literal value", self.column, self.line)
        value = self.parse_primary_expression()
        if self.get().type != TT.open_brace:
            return SyntaxError(self.file_path, self, "Expected a '{' after the match value.", self.column, self.line)
        self.eat()
        body = []
        while self.get().type != TT.close_brace:
            statement = self.parse_statement()
            if isinstance(statement, Error):
                return statement
            if statement:
                body.append(statement)
            if self.get().type == TT.eof:
                return SyntaxError(self.file_path, self, "Expected a '}'", self.column, self.line)
        self.eat()
        return CaseNode(value, body, self.line, self.column)

    def parse_throw_statement(self) -> None:
        self.eat()

        if self.get().type != TT.identifier:
            return SyntaxError(self.file_path, self, "Expected an identifier", self.column, self.line)
        err = self.parse_primary_expression()
        if isinstance(err, Error):
            return err
        if self.get().type != TT.string_value:
            return SyntaxError(self.file_path, self, "Expected a message", self.column, self.line)
        msg = self.parse_primary_expression()
        if isinstance(msg, Error):
            return msg
        return ThrowNode(err, msg, self.line, self.column)
    
    def parse_try_statement(self) -> None:
        self.eat()

        if self.get().type != TT.open_brace:
            return SyntaxError(self.file_path, self, "Expected a '{'", self.column, self.line)
        self.eat()
        tryBody = []
        while self.get().type != TT.close_brace:
            statement = self.parse_statement()
            if isinstance(statement, Error):
                return statement
            if statement:
                tryBody.append(statement)
            if self.get().type == TT.eof:
                return SyntaxError(self.file_path, self, "Expected a '}'", self.column, self.line)
        self.eat()
        if self.get().type != TT.catch:
            return SyntaxError(self.file_path, self, "'catch' expected after 'try'", self.column, self.line)
        self.eat()
        if self.get().type != TT.open_parenthesis:
            return SyntaxError(self.file_path, self, "'(' expected after catch", self.column, self.line)
        self.eat()
        if self.get().type != TT.identifier:
            return SyntaxError(self.file_path, self, "Expected an identifier after 'catch'", self.column, self.line)
        catch = self.parse_primary_expression()
        if isinstance(catch, Error):
            return catch
        if self.get().type != TT.close_parenthesis:
            return SyntaxError(self.file_path, self, "Expected a ')'", self.column, self.line)
        self.eat()
        if self.get().type != TT.open_brace:
            return SyntaxError(self.file_path, self, "Expected a '{' after the exception name.", self.column, self.line)
        self.eat()
        exceptBody = []
        while self.get().type != TT.close_brace:
            statement = self.parse_statement()
            if isinstance(statement, Error):
                return statement
            if statement:
                exceptBody.append(statement)
            if self.get().type == TT.eof:
                return SyntaxError(self.file_path, self, "Expected a '}'", self.column, self.line)
        self.eat()
        return TryNode(tryBody, catch, exceptBody, self.line, self.column)

    def parse_do_while_statement(self) -> None:
        self.eat()

        operand = ''
        if self.get().type != TT.open_brace:
            return SyntaxError(self.file_path, self, "Expected a '{'", self.column, self.line)

        self.eat()
        body = []
        while self.get().type != TT.close_brace:
            statement = self.parse_statement()
            if isinstance(statement, Error):
                return statement
            if statement:
                body.append(statement)
            if self.get().type == TT.eof:
                return SyntaxError(self.file_path, self, "Expected a '}'", self.column, self.line)
        self.eat()
        if self.get().type != TT._while:
            return SyntaxError(self.file_path, self, "Expected a 'while'", self.column, self.line)
        self.eat()
        if self.get().type != TT.open_parenthesis:
            return SyntaxError(self.file_path, self, "Expected a '('", self.column, self.line)
        self.eat()
        left_condition = self.parse_expression()
        if isinstance(left_condition, Error):
            return left_condition
        if self.get().type in self.conditional_operators:
            operand = self.eat().value
            right_condition = self.parse_expression()
            if isinstance(right_condition, Error):
                return right_condition
        else:
            right_condition = NullValue()
        if self.get().type == TT.close_parenthesis:
            self.eat()
        else:
            return SyntaxError(self.file_path, self, "Expected a ')'", self.column, self.line)
        return DoWhileStatementNode(body, left_condition, operand, right_condition, self.line, self.column)

    def parse_while_statement(self) -> None:
        self.eat()

        operand = ''
        if self.get().type != TT.open_parenthesis:
            return SyntaxError(self.file_path, self, "Expected a '('", self.column, self.line)
        self.eat()
        left_condition = self.parse_expression()
        if isinstance(left_condition, Error):
            return left_condition
        if self.get().type in self.conditional_operators:
            operand = self.eat().value
            right_condition = self.parse_expression()
            if isinstance(right_condition, Error):
                return right_condition
        else:
            right_condition = NullValue()

        if self.get().type != TT.close_parenthesis:
            return SyntaxError(self.file_path, self, "Expected a ')'", self.column, self.line)
        self.eat()
        if self.get().type != TT.open_brace:
            return SyntaxError(self.file_path, self, "Expected a '{'", self.column, self.line)
        self.eat()
        body = []
        while self.get().type != TT.close_brace:
            statement = self.parse_statement()
            if isinstance(statement, Error):
                return statement
            if statement:
                body.append(statement)
            if self.get().type == TT.eof:
                return SyntaxError(self.file_path, self, "Expected a '}'", self.column, self.line)
        self.eat()
        if self.get().type != TT._else:
            return WhileStatementNode(left_condition, operand, right_condition, body)
        self.eat()
        if self.get().type != TT.open_brace:
            return SyntaxError(self.file_path, self, "Expected a '{'", self.column, self.line)
        self.eat()
        elseBody = []
        while self.get().type != TT.close_brace:
            statement = self.parse_statement()
            if isinstance(statement, Error):
                return statement
            if statement:
                elseBody.append(statement)
            if self.get().type == TT.eof:
                return SyntaxError(self.file_path, self, "Expected a '}'", self.column, self.line)
        self.eat()
        return WhileStatementNode(left_condition, operand, right_condition, body, elseBody, self.line, self.column)

    def parse_for_statement(self) -> None:
        self.eat()

        if self.get().type == TT.open_parenthesis:
            self.eat()
            declaration = self.parse_variable_declaration()
            if isinstance(declaration, Error):
                return declaration
            if self.get().type != TT.comma:
                return SyntaxError(self.file_path, self, "Expected a comma", self.column, self.line)
            self.eat()
            left_condition = self.parse_expression()
            if isinstance(left_condition, Error):
                return left_condition
            if self.get().type not in self.conditional_operators:
                return SyntaxError(self.file_path, self, f"Expected one of the following operators: {self.conditional_operators}", self.column, self.line)
            operand = self.eat().value
            right_condition = self.parse_expression()
            if isinstance(right_condition, Error):
                return right_condition
            if self.get().type != TT.comma:
                return SyntaxError(self.file_path, self, "Expected a comma after the condition", self.column, self.line)
            self.eat()
            step = self.parse_expression()
            if isinstance(step, Error):
                return step
            if self.get().type != TT.close_parenthesis:
                return SyntaxError(self.file_path, self, "Expected a ')'", self.column, self.line)
            self.eat()
            if self.get().type != TT.open_brace:
                return SyntaxError(self.file_path, self, "Expected a '{'", self.column, self.line)
            self.eat()
            body = []
            while self.get().type != TT.close_brace:
                statement = self.parse_statement()
                if isinstance(statement, Error):
                    return statement
                if statement:
                    body.append(statement)
                if self.get().type == TT.eof:
                    return SyntaxError(self.file_path, self, "Expected a '}'", self.column, self.line)
            self.eat()
        elif self.get().type == TT.each:
            return self.parse_for_each_statement()
        else:
            return SyntaxError(self.file_path, self, "Expected a '(' after 'for'", self.column, self.line)
        return ForStatementNode(declaration, left_condition, operand, right_condition, step, body, self.line, self.column)

    def parse_for_each_statement(self) -> None:
        self.eat()

        if self.get().type != TT.open_parenthesis:
            return SyntaxError(self.file_path, self, "Expected a '('", self.column, self.line)

        self.eat()
        if self.get().type not in ("int", "real", "string"):
            return SyntaxError(self.file_path, self, "Expected variable declaration", self.column, self.line)
        declaration = self.parse_variable_declaration()
        if isinstance(declaration, Error):
            return declaration
        if self.get().type != TT._in:
            return SyntaxError(self.file_path, self, "'in' expected after the variable in for-each loop", self.column, self.line)
        self.eat()
        iterable = self.parse_expression()
        if isinstance(iterable, Error):
            return iterable
        if self.get().type != TT.close_parenthesis:
            return SyntaxError(self.file_path, self, "Expected a ')'", self.column, self.line)
        self.eat()
        if self.get().type != TT.open_brace:
            return SyntaxError(self.file_path, self, "Expected a '{'", self.column, self.line)
        self.eat()
        body = []
        while self.get().type != TT.close_brace:
            statement = self.parse_statement()
            if isinstance(statement, Error):
                return statement
            if statement:
                body.append(statement)
            if self.get().type == TT.eof:
                return SyntaxError(self.file_path, self, "Expected a '}'", self.column, self.line)
        self.eat()
        return ForEachStatementNode(declaration, iterable, body, self.line, self.column)

    def parse_if_statement(self) -> None:
        self.eat()

        operand = ''
        if self.get().type != TT.open_parenthesis:
            return SyntaxError(self.file_path, self, "Expected a '('", self.column, self.line)
        self.eat()
        left_condition = self.parse_expression()
        if isinstance(left_condition, Error):
            return left_condition
        if self.get().type in self.conditional_operators:
            operand = self.eat().value
            right_condition = self.parse_expression()
            if isinstance(right_condition, Error):
                return right_condition
        else:
            right_condition = NullValue()

        if self.get().type == TT.close_parenthesis:
            self.eat()
            if self.get().type != TT.open_brace:
                return SyntaxError(self.file_path, self, "Expected a '{'", self.column, self.line)
            self.eat()
            body = []
            while self.get().type != TT.close_brace:
                statement = self.parse_statement()
                if isinstance(statement, Error):
                    return statement
                if statement:
                    body.append(statement)
                if self.get().type == TT.eof:
                    return SyntaxError(self.file_path, self, "Expected a '}'", self.column, self.line)
            self.eat()
            if self.get().type != TT._else:
                return IfStatementNode(left_condition, operand, right_condition, body)
            self.eat()
            if self.get().type != TT.open_brace:
                return SyntaxError(self.file_path, self, "Expected a '{'", self.column, self.line)
            self.eat()
            else_body = []
            while self.get().type != TT.close_brace:
                statement = self.parse_statement()
                if isinstance(statement, Error):
                    return statement
                if statement:
                    else_body.append(statement)
                if self.get().type == TT.eof:
                    return SyntaxError(self.file_path, self, "Expected a '}'", self.column, self.line)
            self.eat()
        return IfStatementNode(left_condition, operand, right_condition, body, else_body, self.line, self.column)

    def parse_function_declaration(self) -> None:
        self.eat()
        if self.get().type in (TT.identifier, TT.anonymous):
            name = self.eat().value
        else:
            return SyntaxError(self.file_path, self, "Expected a name", self.column, self.line)

        args = self.parse_arguments()
        if isinstance(args, Error):
            return args
        parameters = []
        for parameter in args:
            if parameter.kind == "identifier":
                parameters.append(parameter)
            else:
                return SyntaxError(self.file_path, self, "Expected parameters to be of string type.", self.column, self.line)

        if self.get().type == TT.open_brace:
            self.eat()
        else:
            return SyntaxError(self.file_path, self, "Expected a '{'", self.column, self.line)

        body = []
        while self.get().type != TT.close_brace:
            statement = self.parse_statement()
            if isinstance(statement, Error):
                return statement
            if statement:
                body.append(statement)
            if self.get().type == TT.eof:
                return SyntaxError(self.file_path, self, "Expected a '}'", self.column, self.line)

        self.eat()

        return FunctionDeclarationExpressionNode(str(name), parameters, body, self.line, self.column)

    def parse_variable_declaration(self) -> None:
        datatype = self.eat().type
        if self.get().type == TT.eof:
            return SyntaxError(self.file_path, self, "Expected an identifier", self.column, self.line)
        identifier = self.eat().value
        constant = bool(identifier.isupper())
        if self.get().type != TT.assignment_operator:
            if self.get().type in (TT.eof, TT.lineend):
                self.eat()
            if datatype in ("int", "string", "real", "array", "object", "bool", "lambda", "unknown"):
                return VariableDeclarationExpressionNode(datatype, identifier, self.datatypeMap[datatype], constant, self.line, self.column)
            else:
                return SyntaxError(self.file_path, self, "Expected a variable declaration", self.column, self.line)
        else:
            self.eat()
            statement = self.parse_statement()
            if isinstance(statement, Error):
                return statement
            return VariableDeclarationExpressionNode(datatype, identifier, statement, constant, self.line, self.column)

    def parse_assignment_expression(self) -> None:
        left = self.parse_object_expression()
        if isinstance(left, Error):
            return left

        if self.get().type == TT.assignment_operator:
            self.eat()
            value = self.parse_statement()
            if isinstance(value, Error):
                return value
            return AssignmentExpressionNode(left, value)
        elif self.get().type == TT.assignment_binary_operation:
            operand = self.eat().value
            value = self.parse_expression()
            if isinstance(value, Error):
                return value
            return AssignmentBinaryExpressionNode(left, operand, value, self.line, self.column)
        else:
            return left

    def parse_object_expression(self) -> None:
        if self.get().type != TT.open_brace:
            return self.parse_array_expression()
        else:
            self.eat()

        properties = []

        while self.get().type != TT.eof:
            if self.get().type == TT.close_brace:
                break
            elif self.get().type == TT.lineend:
                self.eat()
                continue
            elif self.get().type == TT.identifier:
                key = self.eat().value
                if self.get().type != TT.colon:
                    return SyntaxError(self.file_path, self, "Expected a value", self.column, self.line)
                self.eat()
                value = self.parse_statement()
                if isinstance(value, Error):
                    return value
                properties.append(PropertyLiteralNode(key, value))
                if self.get().type in (TT.comma, TT.lineend):
                    self.eat()
                elif self.get().type == TT.close_brace:
                    break
                else:
                    return SyntaxError(self.file_path, self, "Expected a ',' or a '}'", self.column, self.line)
            else:
                return SyntaxError(self.file_path, self, "Something went wrong", self.column, self.line)
        self.eat()
        return ObjectLiteralNode(properties, self.line, self.column)

    def parse_array_expression(self) -> None:
        if self.get().type != TT.open_bracket:
            return self.parse_additive_expression()
        else:
            self.eat()

        items = []
        index = -1

        while self.get().type != TT.eof:
            if self.get().type == TT.close_bracket:
                break
            elif self.get().type == TT.lineend:
                self.eat()
                continue
            else:
                index += 1
                value = self.parse_expression()
                if isinstance(value, Error):
                    return value
                items.append(ItemLiteralNode(index, value))
                if self.get().type in (TT.comma, TT.lineend):
                    self.eat()
                elif self.get().type == TT.close_bracket:
                    break
                else:
                    return SyntaxError(self.file_path, self, "Expected a ',' or a ']'", self.column, self.line)
        self.eat()
        return ArrayLiteralNode(items, self.line, self.column)

    def parse_additive_expression(self) -> None:
        left = self.parse_multiplicative_expression()
        if isinstance(left, Error):
            return left

        while self.get().value in ['+', '-',]:
            operand = self.eat().value
            right = self.parse_multiplicative_expression()
            if isinstance(right, Error):
                return right
            left = BinaryExpressionNode(
                left, str(operand), right, self.line, self.column)

        return left

    def parse_multiplicative_expression(self) -> None:
        left = self.parse_call_member_expression()
        if isinstance(left, Error):
            return left

        while self.get().value in ['*', '/', '^', '%', '//']:
            operand = self.eat().value
            right = self.parse_call_member_expression()
            if isinstance(right, Error):
                return right
            left = BinaryExpressionNode(
                left, str(operand), right, self.line, self.column)

        return left

    def parse_call_member_expression(self) -> None:
        member = self.parse_member_expression()
        if isinstance(member, Error):
            return member

        if self.get().type == TT.open_parenthesis:
            return self.parse_call_expression(member)
        return member

    def parse_call_expression(self, caller) -> None:
        value = self.parse_arguments()
        if isinstance(value, Error):
            return value
        call_expression = CallExpression(caller, value, self.line, self.column)

        if self.get().type == TT.open_parenthesis:
            call_expression = self.parse_call_expression(call_expression)
            if isinstance(call_expression, Error):
                return call_expression

        return call_expression

    def parse_arguments(self) -> None:
        if self.get().type == TT.open_parenthesis:
            self.eat()
            args = []
            if self.get().type == TT.close_parenthesis:
                self.eat()
                return []
            else:
                args = self.parse_arguments_list()
                if isinstance(args, Error):
                    return args
        if self.get().type == TT.close_parenthesis:
            self.eat()
        else:
            return SyntaxError(self.file_path, self, "Expected a ')'", self.column, self.line)

        return args

    def parse_arguments_list(self) -> None:
        args = [self.parse_assignment_expression()]
        if isinstance(args[0], Error):
            return args[0]

        while (self.get().type == TT.comma):
            self.eat()
            value = self.parse_assignment_expression()
            if isinstance(value, Error):
                return value
            args.append(value)

        return args

    def parse_member_expression(self) -> None:
        obj = self.parse_primary_expression()
        if isinstance(obj, Error):
            return obj

        while self.get().type in [TT.period, TT.open_bracket]:
            operand = self.eat()

            if operand.type == TT.period:
                computed = True
                prop = self.parse_primary_expression()
                if prop != None:
                    if isinstance(prop, Error):
                        return prop
                    if prop.kind != ("identifier"):
                        return SyntaxError(self.file_path, self, "Invalid syntax", self.column, self.line)
            else:
                computed = False
                prop = self.parse_expression()
                if isinstance(prop, Error):
                    return prop
                if self.get().type != TT.close_bracket:
                    return SyntaxError(self.file_path, self, "Expected a ']'", self.column, self.line)
                else:
                    self.eat()

            obj = MemberExpressionNode(
                obj, prop, computed, self.line, self.column)
        return obj

    def parse_primary_expression(self) -> None:
        match self.get().type:
            case TT.int_value:
                return IntegerLiteralNode(
                    int(self.eat().value), self.line, self.column
                )
            case TT.real_value:
                return RealLiteralNode(
                    float(self.eat().value), self.line, self.column
                )
            case TT.string_value:
                return StringLiteralNode(self.eat().value, self.line, self.column)
            case TT._break:
                self.eat()
                return BreakNode(self.line, self.column)
            case TT._continue:
                self.eat()
                return ContinueNode(self.line, self.column)
            case TT.identifier:
                return IdentifierNode(
                    str(self.eat().value), self.line, self.column
                )
            case TT.open_parenthesis:
                self.eat()
                value = self.parse_expression()
                if isinstance(value, Error):
                    return value
                self.eat()
                return value
            case TT.lineend:
                self.eat()
            case TT._return:
                self.eat()
                value = self.parse_statement()
                if isinstance(value, Error):
                    return value
                return ReturnNode(value, self.line, self.column)
            case TT.export:
                self.eat()
                value = self.parse_statement()
                if isinstance(value, Error):
                    return value
                return ExportNode(value, self.line, self.column)
            case TT._import:
                self.eat()
                names = []
                values = []
                while self.get().type != TT.lineend:
                    if self.get().type not in (TT.identifier, TT.string_value):
                        return SyntaxError(
                            self.file_path,
                            self,
                            "Expected an identifier or a stringValue",
                            self.column,
                            self.line,
                        )

                    value = self.parse_primary_expression()
                    name = value
                    if isinstance(name, Error):
                        return name
                    values.append(name)
                    if self.get().type == TT._as:
                        self.eat()
                        name = self.parse_primary_expression()
                        names.append(name)
                    elif self.get().type == TT.comma:
                        self.eat()
                        names.append(name)
                    else:
                        names.append(name)
                        break
                return ImportNode(names, values, self.line, self.column)

            case _:

                return SyntaxError(
                    self.file_path,
                    self,
                    f"Invalid token '{self.eat().type}' found",
                    self.column,
                    self.line,
                )
