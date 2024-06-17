from frontend.ASTNodes import *
from frontend.Error import *
from backend.RuntimeValue import *
from backend.Environment import Environment, create_global_environment
import os

boolean_table = {
    "T": True,
    "F": False
}

value_type_table = {
    "integerValue": ["integerValue", "realValue", "unknownValue"],
    "realValue": ["realValue", "integerValue", "unknownValue"],
    "stringValue": ["stringValue", "unknownValue"],
    "arrayValue": ["arrayValue", "unknownValue"],
    "nullValue": ["nullValue", "unknownValue"],
    "booleanValue": ["booleanValue", "unknownValue"],
    "objectValue": ["objectValue", "unknownValue"],
    "functionValue": ["functionValue", "unknownValue"],
    "unknownValue": ["integerValue", "realValue", "booleanValue", "objectValue", "function", "stringValue", "nullValue", "arrayValue", "unknownValue"]
}


class Interpreter:
    def __init__(self, file_path: str = "") -> None:
        self.file_path = file_path

    def __str__(self) -> str:
        return "Interpreter"

    def check_condition(self, left: RuntimeValue, operand: str, right: RuntimeValue) -> bool:
        res = False
        if isinstance(right, NullValue):
            if isinstance(left, (RealValue, IntegerValue)):
                res = BooleanValue("T") if left.value != 0 else BooleanValue("F")
            elif isinstance(left, BooleanValue):
                res = left.value == "T"
            elif isinstance(left, StringValue):
                res = left.value != ""
        elif isinstance(left, (RealValue, IntegerValue)) and isinstance(right, (RealValue, IntegerValue)):
            match operand:
                case "==":
                    res = left.value == right.value
                case ">":
                    res = left.value > right.value
                case "<":
                    res = left.value < right.value
                case ">=":
                    res = left.value >= right.value
                case "<=":
                    res = left.value <= right.value
                case "!=":
                    res = left.value != right.value
        elif isinstance(left, BooleanValue) and isinstance(right, BooleanValue):
            match operand:
                case "&":
                    res = boolean_table[left.value] and boolean_table[right.value]
                case "|":
                    res = boolean_table[left.value] or boolean_table[right.value]
                case "!=":
                    res = boolean_table[left.value] != boolean_table[right.value]
        elif isinstance(left, StringValue) and isinstance(right, StringValue):
            match operand:
                case "==":
                    res = left.value == right.value
                case "!=":
                    res = left.value != right.value
        else:
            return SyntaxError(self.file_path, self, "Invalid contidion", right.column, right.line)
        return res

    def evaluate_program(self, program: ProgramNode, env: Environment) -> NullValue | IntegerValue | ObjectValue | ArrayValue | StringValue | bool | None:
        last_evaluated = NullValue()

        for statement in program.body:
            last_evaluated = self.evaluate(statement, env)
            if isinstance(last_evaluated, Error):
                return last_evaluated

        return last_evaluated

    def evaluate_binary_expression(self, binary_operation: BinaryExpressionNode, env: Environment) -> IntegerValue | NullValue:
        left = self.evaluate(binary_operation.left, env)
        if isinstance(left, Error):
            return left
        right = self.evaluate(binary_operation.right, env)
        if isinstance(right, Error):
            return right

        if isinstance(left, (RealValue, IntegerValue)) and isinstance(right, (RealValue, IntegerValue)):
            return self.evaluate_numeric_binary_expression(left, right, binary_operation.operand)
        elif isinstance(left, StringValue) and isinstance(right, (StringValue, (RealValue, IntegerValue))):
            return self.evaluate_string_binary_expression(left, right, binary_operation.operand)

        elif isinstance(left, ArrayValue):
            return self.evaluate_array_append_binary_expression(left, right, binary_operation.operand)
        else:
            return TypeError(self.file_path, self, f"Incompatible types. '{left.type}' and '{right.type}'", right.column, right.line)

    def evaluate_array_append_binary_expression(self, left: ArrayValue, right, operand: str) -> ArrayValue:
        match operand:
            case "+":
                index = len(left.items)
                left.items[index] = right
                return ArrayValue(left.items)
            case _:
                return SyntaxError(self.file_path, self, "Cannot preform this operation on arrays.", right.column, right.line)

    def evaluate_object_binary_expression(self, left: ObjectValue, right: ObjectValue, operand: str) -> ObjectValue:
        match operand:
            case "+":
                return ObjectValue(left.properties.update(right.properties))
            case _:
                return SyntaxError(self.file_path, self, "Cannot preform this operation on objects.", right.column, right.line)

    def evaluate_array_binary_expression(self, left: ArrayValue, right: ArrayValue, operand: str) -> ArrayValue:
        match operand:
            case "+":
                return ArrayValue(left.items + right.items)
            case _:
                return SyntaxError(self.file_path, self, "Cannot preform this operation on arrays.", right.column, right.line)

    def evaluate_string_binary_expression(self, left: StringValue, right: StringValue | IntegerValue | RealValue, operand: str) -> StringValue:
        match operand:
            case "+":
                return StringValue(left.value + str(right.value))
            case _:
                return SyntaxError(self.file_path, self, "Cannot preform this operation on strings.", right.column, right.line)

    def evaluate_numeric_binary_expression(self, left: IntegerValue | RealValue, right: IntegerValue | RealValue, operand: str) -> RealValue:
        match operand:
            case "+":
                if isinstance(left, RealValue) or isinstance(right, RealValue):
                    return RealValue(left.value + right.value)
                else:
                    return IntegerValue(left.value + right.value)
            case "-":
                if isinstance(left, RealValue) or isinstance(right, RealValue):
                    return RealValue(left.value - right.value)
                else:
                    return IntegerValue(left.value - right.value)
            case "*":
                if isinstance(left, RealValue) or isinstance(right, RealValue):
                    return RealValue(left.value * right.value)
                else:
                    return IntegerValue(left.value * right.value)
            case "/":
                if right.value != 0:
                    return RealValue(left.value / right.value)
                else:
                    return ZeroDivisionError(self.file_path, self, right.column, right.line)
            case "^":
                if isinstance(left, RealValue) or isinstance(right, RealValue):
                    return RealValue(left.value ** right.value)
                else:
                    return IntegerValue(left.value ** right.value)
            case "%":
                if right.value != 0:
                    return IntegerValue(left.value % right.value)
                else:
                    return ZeroDivisionError(self.file_path, self, right.column, right.line)
            case "//":
                if right.value != 0:
                    return IntegerValue(left.value // right.value)
                else:
                    return ZeroDivisionError(self.file_path, self, right.column, right.line)
            case _:
                return SyntaxError(self.file_path, self, "Cannot preform this operation on numbers", right.column, right.line)

# --------------------------------------------------------------------------------------------------------------------------------

    def evaluate_identifier_expression(self, identifier: IdentifierNode, env: Environment) -> None:
        return env.lookup(identifier)

    def evaluate_assignment_expression(self, assignment_expression: AssignmentExpressionNode, env: Environment) -> None:
        if isinstance(assignment_expression.assigne, IdentifierNode):
            return self.process_variable_assignment(
                assignment_expression, env
            )
        elif isinstance(assignment_expression.assigne, MemberExpressionNode):
            member: MemberExpressionNode = assignment_expression.assigne
            varName = member.object
            if assignment_expression.assigne.computed:
                prop = member.property.symbol
            else:
                prop = self.evaluate(member.property, env)
            current_value: dict = env.lookup(varName)
            if isinstance(current_value, Error):
                return current_value
            current_value.properties[prop] = self.evaluate(
                assignment_expression.value, env)
            return env.assign_variable(varName.symbol, current_value)
        else:
            return SyntaxError(self.file_path, self, "Expected an identifier.", assignment_expression.assigne.column, assignment_expression.assigne.line)

    def process_variable_assignment(self, assignment_expression: AssignmentExpressionNode, env: Environment):
        varName = assignment_expression.assigne.symbol
        current_value = env.lookup(assignment_expression.assigne)
        if isinstance(current_value, Error):
            return current_value
        value = self.evaluate(assignment_expression.value, env)

        if isinstance(value, Error):
            return value

        if value.type in value_type_table[value.type]:
            return env.assign_variable(varName, value)
        return TypeError(self.file_path, self, f"'{value.type}' is incompatible with '{current_value.type}'", value.column, value.line)

    def evaluate_variable_declaration_expression(self, declaration: VariableDeclarationExpressionNode, env: Environment) -> None:
        value = self.evaluate(declaration.value, env)
        if isinstance(value, Error):
            return value

        if value.type in value_type_table[value.type]:
            return env.declare_variable(declaration.identifier, value, declaration.constant)
        return TypeError(self.file_path, self, f"'{value.type}' is incompatible with '{declaration.dataType}'", value.column, value.line)

    def evaluate_function_declaration(self, declaration: FunctionDeclarationExpressionNode, env: Environment) -> None:
        fn = Function(declaration.name, declaration.parameters,
                      env, declaration.body)
        return env.declare_variable(declaration.name, fn)

    def evaluate_object_expression(self, object: ObjectLiteralNode, env: Environment) -> ObjectValue:
        properties = {}

        for prop in object.properties:
            a = self.evaluate(prop.value, env)
            if isinstance(a, Error):
                return a
            properties[prop.key] = a
        return ObjectValue(properties, object.line, object.column)

    def evaluate_array_expression(self, array: ArrayLiteralNode, env: Environment) -> ArrayValue:
        items = {item.index: self.evaluate(item.value, env) for item in array.items}
        return ArrayValue(items, array.line, array.column)

    def evaluate_call_expression(self, call_expression: CallExpression, env: Environment) -> NullValue | IntegerValue | ObjectValue | ArrayValue | StringValue | bool | None:
        args = []
        for arg in call_expression.arguments:
            a = self.evaluate(arg, env)
            if isinstance(a, Error):
                return a
            args.append(a)
        fn: NativeFunction | Function = self.evaluate(call_expression.caller, env)
        if isinstance(fn, Error):
            return fn

        if isinstance(fn, NativeFunction):
            return fn.call(args, env)
        elif isinstance(fn, Function):
            scope = create_global_environment(env)

            if len(fn.parameters) == len(args):
                for i in range(len(fn.parameters)):
                    scope.declare_variable(fn.parameters[i].symbol, args[i])
            else:
                if len(fn.parameters) > 0:
                    column = fn.parameters[-1].column
                    line = fn.parameters[-1].line
                else:
                    column = fn.column
                    line = fn.line
                return SyntaxError(self.file_path, self, f"Insufficient arguments provided. Expected {len(fn.parameters)}, but received {len(args)}\nExpected [{', '.join([i.symbol for i in fn.parameters])}]", column, line)

            # Loop through funcion body and evalute the code
            result = NullValue()
            for statement in fn.body:
                result = self.evaluate(statement, scope)
                if isinstance(result, Error):
                    return result
                if isinstance(statement, ReturnNode):
                    return result
        else:
            return SyntaxError(self.file_path, self, f"'{fn.type}' is not a function", fn.column, fn.line)
        return NullValue()

    def evaluate_member_expression(self, member: MemberExpressionNode, env: Environment) -> None:
        x = self.evaluate(member.object, env) if isinstance(member.object, (MemberExpressionNode, StringLiteralNode)) else member.object

        if isinstance(x, Error):
            return x

        obj = x if isinstance(x, (ObjectValue, ArrayValue, StringValue)) else env.lookup(x)

        if isinstance(obj, ObjectValue):
            if isinstance(member.property, IdentifierNode):
                if isinstance(list(obj.properties.keys())[0], StringValue):
                    obj.properties = {key.value: value for key, value in obj.properties.items() if isinstance(key, StringValue)}

                if method_or_property := obj.methods.get(
                    member.property.symbol
                ) or obj.properties.get(member.property.symbol):
                    return method_or_property

                v = self.evaluate(member.property, env)
                if isinstance(v, Error):
                    return v
                return obj.properties.get(v.value, KeyError(self.file_path, self, v, obj, v.column, v.line))

            if isinstance(member.property, StringLiteralNode):
                return obj.properties.get(member.property.value, TypeError(self.file_path, self, f"Expected an identifier or a string value got {member.property}", self.column, self.line))

        if isinstance(obj, (ArrayValue, StringValue)):
            if isinstance(member.property, IntegerLiteralNode):
                return obj.items.get(member.property.value, KeyError(self.file_path, self, member.property.value, member.object.symbol, member.property.column, member.property.line))

            if isinstance(member.property, IdentifierNode):
                if method := obj.methods.get(member.property.symbol):
                    return method

                value = self.evaluate(member.property, env)
                if isinstance(value, Error):
                    return value

                return obj.items.get(value.value, SyntaxError(self.file_path, self, f"'{member.property.symbol}' is not a valid method or property.", member.column, member.line))

        return KeyError(self.file_path, self, member.property.symbol, member.object.symbol, member.property.column, member.property.line)


    def evaluate_if_statement(self, if_statement: IfStatementNode, env: Environment) -> None:
        left: RuntimeValue = self.evaluate(if_statement.left_condition, env)
        if isinstance(left, Error):
            return left
        if not isinstance(if_statement.right_condition, NullValue):
            right: RuntimeValue = self.evaluate(
                if_statement.right_condition, env)
            if isinstance(right, Error):
                return right
        else:
            right = NullValue()

        res = False
        if res := self.check_condition(left, if_statement.operand, right):
            result = NullValue()
            for statement in if_statement.body:
                if isinstance(statement, (ContinueNode, BreakNode)):
                    return statement
                result = self.evaluate(statement, env)
                if isinstance(result, (Error, ReturnNode)):
                    return result
        elif if_statement.else_body != []:
            result = NullValue()
            for statement in if_statement.else_body:
                if isinstance(statement, (ContinueNode, BreakNode)):
                    return statement
                result = self.evaluate(statement, env)
                if isinstance(result, (Error, ReturnNode)):
                    return result
        return NullValue()

    def evaluate_while_statement(self, while_statement: WhileStatementNode, env: Environment) -> bool:
        while True:
            left: RuntimeValue = self.evaluate(
                while_statement.left_condition, env)
            if isinstance(left, Error):
                return left
            if not isinstance(while_statement.right_condition, NullValue):
                right: RuntimeValue = self.evaluate(
                    while_statement.right_condition, env)
                if isinstance(right, Error):
                    return right
            else:
                right = NullValue()

            res = False
            if res := self.check_condition(left, while_statement.operand, right):
                result = NullValue()
                for statement in while_statement.body:
                    if isinstance(statement, (Error, ReturnNode, BreakNode)):
                        return result
                    if isinstance(result, ContinueNode):
                        break
                    result = self.evaluate(statement, env)
                    if isinstance(result, (Error, BreakNode)):
                        return result
                    if isinstance(result, ContinueNode):
                        break
            else:
                if while_statement.else_body != []:
                    result = NullValue()
                    for statement in while_statement.else_body:
                        if isinstance(result, (Error, ReturnNode, BreakNode)):
                            return result
                        if isinstance(result, ContinueNode):
                            break
                        result = self.evaluate(statement, env)
                        if isinstance(result, (Error, BreakNode)):
                            return result
                        if isinstance(result, ContinueNode):
                            break
                break
        return NullValue()

    def evaluate_for_statement(self, for_statement: ForStatementNode, env: Environment) -> None:
        self.evaluate_variable_declaration_expression(for_statement.declaration, env)

        while True:
            left: RuntimeValue = self.evaluate(for_statement.left_condition, env)
            if isinstance(left, Error):
                return left
            if not isinstance(for_statement.right_condition, NullValue):
                right: RuntimeValue = self.evaluate(
                    for_statement.right_condition, env)
                if isinstance(right, Error):
                    return right
            else:
                right = NullValue()

            res = False
            if not (res := self.check_condition(left, for_statement.operand, right)):
                break
            result = NullValue()
            for statement in for_statement.body:
                if isinstance(statement, (Error, ReturnNode, BreakNode)):
                    return result
                result = self.evaluate(statement, env)
                if isinstance(result, (Error, BreakNode)):
                    return result
                if isinstance(result, ContinueNode):
                    break
            result = self.evaluate_assignment_binary_expression(
                for_statement.step, env)
        return NullValue()

    def evaluate_for_each_statement(self, for_each_statement: ForEachStatementNode, env: Environment) -> None:
        self.evaluate_variable_declaration_expression(
            for_each_statement.declaration, env)

        array = self.evaluate(for_each_statement.iterable, env)

        for item in array.items:
            assignment_expression = AssignmentExpressionNode(IdentifierNode(
                for_each_statement.declaration.identifier, for_each_statement.declaration.line, for_each_statement.declaration.column), IntegerLiteralNode(array.items[item].value, -1, -1))
            res = self.evaluate_assignment_expression(assignment_expression, env)
            if isinstance(res, Error):
                return res

            result = NullValue()
            for statement in for_each_statement.body:
                if isinstance(statement, (Error, ReturnNode, BreakNode)):
                    return result
                result = self.evaluate(statement, env)
                if isinstance(result, (Error, BreakNode)):
                    return result
                if isinstance(result, ContinueNode):
                    break

        return NullValue()

    def evaluate_do_while_statement(self, do_while_statement: DoWhileStatementNode, env: Environment) -> None:
        res = True
        while res:
            result = NullValue()
            for statement in do_while_statement.body:
                if isinstance(statement, (ReturnNode, Error, BreakNode)):
                    return result
                if isinstance(statement, ContinueNode):
                    break
                result = self.evaluate(statement, env)
                if isinstance(result, (Error, BreakNode)):
                    return result
                if isinstance(result, ContinueNode):
                    break

            left: RuntimeValue = self.evaluate(do_while_statement.conditionLeft, env)
            if isinstance(left, Error):
                return result
            if not isinstance(do_while_statement.conditionRight, NullValue):
                right: RuntimeValue = self.evaluate(
                    do_while_statement.conditionRight, env)
                if isinstance(right, Error):
                    return result
            else:
                right = NullValue()

            res = self.check_condition(left, do_while_statement.operand, right)
        return NullValue()

    def evaluate_return_expression(self, return_expression: ReturnNode, env: Environment):
        return self.evaluate(return_expression.value, env)

    def evaluate_assignment_binary_expression(self, expr: AssignmentBinaryExpressionNode, env: Environment) -> None:
        currValue = env.lookup(expr.assigne)
        if isinstance(currValue, IntegerValue):
            current_value = IntegerLiteralNode(
                currValue.value, expr.column, expr.line)
        elif isinstance(currValue, RealValue):
            current_value = RealLiteralNode(
                currValue.value, expr.column, expr.line)
        elif isinstance(currValue, StringValue):
            current_value = StringLiteralNode(
                currValue.value, expr.column, expr.line)
        else:
            return TypeError(self.file_path, self, f"Incompatible type '{currValue}'", expr.column, expr.line)

        binexpr = BinaryExpressionNode(
            current_value, expr.operand[0], expr.value, expr.line, expr.column)
        newValue = self.evaluate_binary_expression(binexpr, env)

        if isinstance(newValue, Error):
            return newValue
        elif isinstance(newValue, RealValue):
            v = RealLiteralNode(newValue.value, expr.line, expr.column)
        elif isinstance(newValue, IntegerValue):
            v = IntegerLiteralNode(newValue.value, expr.line, expr.column)
        elif isinstance(newValue, StringValue):
            v = StringLiteralNode(newValue.value, expr.column, expr.line)
        else:
            return TypeError(self.file_path, self, f"Incompatible types. '{current_value}' and '{newValue}'", expr.column, expr.line)

        return self.evaluate_assignment_expression(AssignmentExpressionNode(expr.assigne, v), env)

    def evaluate_export_expression(self, export_expression: ExportNode, env: Environment):
        return ExportValue(self.evaluate(export_expression.value, env), export_expression.line, export_expression.column)

    def evaluate_import_expression(self, import_expression: ImportNode, env: Environment):
        from shell import run

        result = NullValue()
        for i in range(len(import_expression.values)):
            path = import_expression.values[i]

            if isinstance(path, IdentifierNode):
                path = path.symbol
            elif isinstance(path, StringValue):
                path = path.value
            else:
                return SyntaxError(self.file_path, self, "Expected an identifier or a stringValue", import_expression.column, import_expression.line)

            name = import_expression.names[i].symbol
            path = path.lower()
            path = f"Modules/{path}"

            module = ObjectValue({})

            if os.path.exists(path):
                self.proccess_successful_import(env, path, name, module)
            else:
                path = import_expression.values[i]

                if isinstance(path, IdentifierNode):
                    path = path.symbol
                elif isinstance(path, StringValue):
                    path = path.value
                else:
                    return SyntaxError(self.file_path, self, "Expected an identifier or a stringValue", import_expression.column, import_expression.line)

                name = import_expression.names[i].symbol
                directory = "/".join(self.file_path.split("/")[:-1])
                file = f"{directory}/{path.lower()}.phi"

                if not os.path.exists(file):
                    return FileNotFoundError(self.file_path, self, f"{path}", import_expression.column, import_expression.line)
                with open(file, "r") as f:
                    code = "\n".join(f.readlines())

                code = run(code, file)
                if isinstance(code, ExportValue):
                    result = (
                        env.declare_variable(name, code.value, True)
                        if name.isupper()
                        else env.declare_variable(name, code.value, False)
                    )
        return result

    def proccess_successful_import(self, env, path, name, module):
        from shell import run
        filenames = [f for f in os.listdir(path) if os.path.isfile(
                    os.path.join(path, f))]

        for file in filenames:
            if file.endswith(".phi"):
                n = file.split(".")[0]
                file = f"{path}/{file}"

                with open(file, "r") as f:
                    code = "\n".join(f.readlines())

                code = run(code, file)
                if isinstance(code, ExportValue):
                    module.properties.update({n: code.value})

        if name.isupper():
            result = env.declare_variable(name, module, True)
        else:
            result = env.declare_variable(name, module, False)

    def evaluate_try_statement(self, try_statement: TryNode, env: Environment) -> None:
        result = NullValue()
        for statement in try_statement.try_body:
            if isinstance(statement, (ReturnNode, Error, BreakNode)):
                break
            if isinstance(statement, ContinueNode):
                break
            result = self.evaluate(statement, env)
            if isinstance(result, (Error, BreakNode)):
                break
            if isinstance(result, ContinueNode):
                break

        if not isinstance(result, Error):
            return result
        if result.type != try_statement.exception.symbol:
            return result
        result = NullValue()
        for statement in try_statement.exceptBody:
            if isinstance(statement, (Error, BreakNode)):
                return statement
            if isinstance(statement, ContinueNode):
                break
            result = self.evaluate(statement, env)
            if isinstance(result, (Error, BreakNode)):
                return result
            if isinstance(result, ContinueNode):
                break

    def evaluate_throw_statement(self, throw_statement: ThrowNode, env: Environment) -> None:
        match throw_statement.error.symbol:
            case "syntaxError":
                return SyntaxError(self.file_path, "", throw_statement.msg.value, throw_statement.column, throw_statement.line)
            case "zeroDivisionError":
                return ZeroDivisionError(self.file_path, "", throw_statement.column, throw_statement.line)
            case "typeError":
                return TypeError(self.file_path, "", throw_statement.msg.value, throw_statement.column, throw_statement.line)
            case "keyError":
                return KeyError(self.file_path, "", "", "", throw_statement.column, throw_statement.line)
            case "notImplementedError":
                return NotImplementedError(self.file_path, "", throw_statement.msg.value, throw_statement.column, throw_statement.line)
            case "invalidCharacterError":
                return InvalidCharacterError(self.file_path, "", throw_statement.msg.value, throw_statement.column, throw_statement.line)
            case "nameError":
                return NameError(self.file_path, "", throw_statement.msg.value, throw_statement.column, throw_statement.line)

    def evaluate_match_statement(self, match_statement: MatchNode, env: Environment) -> None:
        value = self.evaluate(match_statement.value, env)

        for match in match_statement.matches:
            v = self.evaluate(match.value, env)
            if value.value == v.value:
                result = NullValue()
                for statement in match.body:
                    if isinstance(statement, (Error, BreakNode)):
                        return statement
                    if isinstance(statement, ContinueNode):
                        break
                    result = self.evaluate(statement, env)
                    if isinstance(result, (Error, BreakNode, ReturnNode)):
                        return result
                    if isinstance(result, ContinueNode):
                        break
                return result
        return NullValue()

    def evaluate_delete_statement(self, delete_statement: DeleteNode, env: Environment) -> None:
        env.delete_variable(delete_statement.variable)
        return NullValue()

    def evaluate(self, astNode, env: Environment) -> NullValue | IntegerValue | ObjectValue | ArrayValue | StringValue | None:
        if isinstance(astNode, (str, float, int, Error)):
            return astNode
        match astNode.kind:
            case "program":
                return self.evaluate_program(astNode, env)
            case "binaryExpression":
                return self.evaluate_binary_expression(astNode, env)
            case "identifier":
                return self.evaluate_identifier_expression(astNode, env)
            case "assignmentExpression":
                return self.evaluate_assignment_expression(astNode, env)
            case "variableDeclarationExpression":
                return self.evaluate_variable_declaration_expression(astNode, env)
            case "functionDeclaration":
                return self.evaluate_function_declaration(astNode, env)
            case "objectLiteral":
                return self.evaluate_object_expression(astNode, env)
            case "callExpression":
                return self.evaluate_call_expression(astNode, env)
            case "memberExpression":
                return self.evaluate_member_expression(astNode, env)
            case "ifStatement":
                return self.evaluate_if_statement(astNode, env)
            case "whileStatement":
                return self.evaluate_while_statement(astNode, env)
            case "forStatement":
                return self.evaluate_for_statement(astNode, env)
            case "forEachStatement":
                return self.evaluate_for_each_statement(astNode, env)
            case "doWhileStatement":
                return self.evaluate_do_while_statement(astNode, env)
            case "arrayLiteral":
                return self.evaluate_array_expression(astNode, env)
            case "returnExpression":
                return self.evaluate_return_expression(astNode, env)
            case "assignmentBinaryExpression":
                return self.evaluate_assignment_binary_expression(astNode, env)
            case "exportExpression":
                return self.evaluate_export_expression(astNode, env)
            case "importExpression":
                return self.evaluate_import_expression(astNode, env)
            case "tryStatement":
                return self.evaluate_try_statement(astNode, env)
            case "throwStatement":
                return self.evaluate_throw_statement(astNode, env)
            case "matchStatement":
                return self.evaluate_match_statement(astNode, env)
            case "delete":
                return self.evaluate_delete_statement(astNode, env)

            case "integerLiteral":
                return IntegerValue(astNode.value, astNode.line, astNode.column)
            case "realLiteral":
                return RealValue(astNode.value, astNode.line, astNode.column)
            case "stringLiteral":
                return StringValue(astNode.value, astNode.line, astNode.column)
            case "unknownLiteral":
                return UnknownValue(astNode.value, astNode.line, astNode.column)
            case "nullLiteral":
                return NullValue()
            case _:
                return NotImplementedError(self.file_path, self, astNode.kind, astNode.column, astNode.line)
