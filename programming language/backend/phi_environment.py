from frontend.errors import *
from backend.values import *
import backend.builtInFunctions as bif
import sys
from frontend.astNodes import *

class environment:
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

    def assignVariable(self, var_name: str, var_value) -> None:
        if var_name in self.variables:
            self.variables[var_name] = var_value
        elif var_name in self.constants:
            return syntaxError(self.file_path, self, "Can't assign a new value to a constant", 0, 0)
        else:
            return nameError(self.file_path, self, var_name, 0, 0)

        return var_value

    def declareVariable(self, var_name: str, var_value, constant:bool=False) -> None:
        if ((var_name in self.variables) or (var_name in self.constants)) and (var_name != '~'):
            return syntaxError(self.file_path, self, f"Variable '{var_name}' already defined.", 0, 0)
        else:
            if constant:
                self.constants[var_name] = var_value
            else:
                self.variables[var_name] = var_value

        return var_value

    def lookup(self, var:identifierNode) -> None:
        var_name = var.symbol
        env = self.resolve(var_name)
        if isinstance(env, error):
            return env
        if var_name in env.constants:
            return env.constants[var_name]
        elif var_name in env.variables:
            return env.variables[var_name]
        else:
            return nameError(self.file_path, self, var_name, var.column, var.line)

    def resolve(self, var_name: str) -> None:
        if var_name in self.variables:
            return self
        elif var_name in self.constants:
            return self
        
        if self.parent == None:
            return nameError(self.file_path, self, var_name, 0, 0)
        else:
            return self.parent.resolve(var_name)
        
    def deleteVariable(self, var_name:str) -> None:
        env = self.resolve(var_name)
        del env.variables[var_name]


def createGlobalEnvironment(parent:environment|None=None, file_path:str='') -> environment:
    env = environment(parent, file_path)
    # functions
    env.declareVariable('output', nativeFunction(lambda args, scope : sys.stdout.write(str(bif.output(args[0], file_path)) + '\n')), True)
    env.declareVariable('input', nativeFunction(lambda args, scope : bif.input(file_path, args[0])), True)
    env.declareVariable('type', nativeFunction(lambda args, scope : bif.type_(file_path, args[0])), True)
    env.declareVariable('hash', nativeFunction(lambda args, scope : bif.hash(file_path, args[0])), True)
    env.declareVariable('Str', nativeFunction(lambda args, scope: bif.hardCastStr(file_path, args[0])), True)
    env.declareVariable('Int', nativeFunction(lambda args, scope: bif.hardCastInt(file_path, args[0])), True)
    env.declareVariable('Real', nativeFunction(lambda args, scope: bif.hardCastReal(file_path, args[0])), True)
    env.declareVariable('readFile', nativeFunction(lambda args, scope: bif.readFile(file_path, args[0], args[1])), True)

    # Move to modules
    env.declareVariable('now', nativeFunction(lambda args, scope : bif.now(file_path, )), True)
    env.declareVariable('wait', nativeFunction(lambda args, scope : bif.wait(file_path, args[0])), True)

    # variables
    env.declareVariable('_', nullValue(), True)
    env.declareVariable('?', unknownValue(nullValue()))
    env.declareVariable('T', booleanValue("T"), True)
    env.declareVariable('F', booleanValue("F"), True)
    
    return env