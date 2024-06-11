from frontend.errors import *
from backend.values import *
from backend.built_in_functions import *
import sys
from frontend.ast_nodes import *

class Environment:
    def __init__(self, parent=None, file_path:str='') -> None:
        self.file_path = file_path
        self.parent = parent
        self.variables = {}
        self.constants = {}

    def __str__(self) -> str:
        return 'Environment'

    def __repr__(self) -> str:
        return str({
            "parent":self.parent,
            "variables":self.variables
        })

    def assign_variable(self, variable_name: str, var_value) -> None:
        if variable_name in self.variables:
            self.variables[variable_name] = var_value
        elif variable_name in self.constants:
            return SyntaxError(self.file_path, self, "Can't assign a new value to a constant", 0, 0)
        else:
            return NameError(self.file_path, self, variable_name, 0, 0)

        return var_value

    def declare_variable(self, variable_name: str, var_value, constant:bool=False) -> None:
        if ((variable_name in self.variables) or (variable_name in self.constants)) and (variable_name != '~'):
            return SyntaxError(self.file_path, self, f"Variable '{variable_name}' already defined.", 0, 0)
        if constant:
            self.constants[variable_name] = var_value
        else:
            self.variables[variable_name] = var_value

        return var_value

    def lookup(self, variable:IdentifierNode) -> None:
        var_name = variable.symbol
        env = self.resolve(var_name)
        if isinstance(env, Error):
            return env
        if var_name in env.constants:
            return env.constants[var_name]
        elif var_name in env.variables:
            return env.variables[var_name]
        else:
            return NameError(self.file_path, self, var_name, variable.column, variable.line)

    def resolve(self, variable_name: str) -> None:
        if variable_name in self.variables or variable_name in self.constants:
            return self
        if self.parent is None:
            return NameError(self.file_path, self, variable_name, 0, 0)
        else:
            return self.parent.resolve(variable_name)
        
    def delete_variable(self, variable_name:str) -> None:
        env = self.resolve(variable_name)
        del env.variables[variable_name]

def create_global_environment(parent:Environment|None=None, file_path:str='') -> Environment:
    env = Environment(parent, file_path)
    # functions
    env.declare_variable('output', NativeFunction(lambda args, scope : sys.stdout.write(str(output(args[0], file_path)) + '\n')), True)
    env.declare_variable('input', NativeFunction(lambda args, scope : input(file_path, args[0])), True)
    env.declare_variable('type', NativeFunction(lambda args, scope : type_(file_path, args[0])), True)
    env.declare_variable('hash', NativeFunction(lambda args, scope : hash(file_path, args[0])), True)
    env.declare_variable('Str', NativeFunction(lambda args, scope: hard_cast_string(file_path, args[0])), True)
    env.declare_variable('Int', NativeFunction(lambda args, scope: hard_cast_integer(file_path, args[0])), True)
    env.declare_variable('Real', NativeFunction(lambda args, scope: hard_cast_real(file_path, args[0])), True)
    env.declare_variable('readFile', NativeFunction(lambda args, scope: read_file(file_path, args[0])), True)

    # Move to modules
    env.declare_variable('now', NativeFunction(lambda args, scope : now(file_path, )), True)
    env.declare_variable('wait', NativeFunction(lambda args, scope : wait(file_path, args[0])), True)

    # variables
    env.declare_variable('_', NullValue(), True)
    env.declare_variable('?', UnknownValue(NullValue()))
    env.declare_variable('T', BooleanValue("T"), True)
    env.declare_variable('F', BooleanValue("F"), True)
    
    return env