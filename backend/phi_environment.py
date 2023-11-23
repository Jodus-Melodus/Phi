from frontend.errors import nameError, syntaxError
from backend.values import *
import backend.builtInFunctions as bif
import sys

class environment:
    def __init__(self, parent=None) -> None:
        self.parent = parent
        self.variables = {}
        self.constants = {}

    def __repr__(self) -> str:
        return str({
            "parent":self.parent,
            "variables":self.variables
        })

    def assignVariable(self, varName: str, varValue) -> None:
        if varName in self.variables:
            self.variables[varName] = varValue
        elif varName in self.constants:
            return syntaxError("Can't assign a new value to a constant")
        else:
            return nameError(varName)

        return varValue

    def declareVariable(self, varName: str, varValue, constant:bool=False) -> None:
        if (varName in self.variables) or (varName in self.constants):
            return syntaxError(f"Variable {varName} already defined.")
        else:
            if constant:
                self.constants[varName] = varValue
            else:
                self.variables[varName] = varValue

        return varValue

    def lookup(self, varName: str) -> None:
        env = self.resolve(varName)
        if varName in self.constants:
            return env.constants[varName]
        elif varName in self.variables:
            return env.variables[varName]
        else:
            return nameError(varName)

    def resolve(self, varName: str) -> None:
        if varName in self.variables:
            return self
        elif varName in self.constants:
            return self
        
        if self.parent == None:
            return nameError(varName)
        else:
            return self.parent.resolve(varName)

def createGlobalEnvironment(parent=None) -> environment:
    env = environment(parent)
    # functions
    env.declareVariable('out', nativeFunction(lambda args, scope : sys.stdout.write(str(bif.out(args[0])) + '\n')), True)
    env.declareVariable('in', nativeFunction(lambda args, scope : bif.in_(args[0])), True)
    env.declareVariable('now', nativeFunction(lambda args, scope : bif.now()), True)
    env.declareVariable('wait', nativeFunction(lambda args, scope : bif.wait(args[0])), True)
    env.declareVariable('type', nativeFunction(lambda args, scope : bif.type_(args[0])), True)
    env.declareVariable('root', nativeFunction(lambda args, scope : bif.root(args[0], args[1])), True)
    env.declareVariable('length', nativeFunction(lambda args, scope : bif.length(args[0])), True)

    # variables
    env.declareVariable('_', nullValue(), True)
    env.declareVariable('T', booleanValue("T"), True)
    env.declareVariable('F', booleanValue("F"), True)
    
    return env