from frontend.errors import *
from backend.values import *
import backend.builtInFunctions as bif
import sys
from frontend.astNodes import *

class environment:
    def __init__(self, parent=None, filePath:str='') -> None:
        self.filePath = filePath
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

    def assignVariable(self, varName: str, varValue) -> None:
        if varName in self.variables:
            self.variables[varName] = varValue
        elif varName in self.constants:
            return syntaxError(self.filePath, self, "Can't assign a new value to a constant", 0, 0)
        else:
            return nameError(self.filePath, self, varName, 0, 0)

        return varValue

    def declareVariable(self, varName: str, varValue, constant:bool=False) -> None:
        if ((varName in self.variables) or (varName in self.constants)) and (varName != '~'):
            return syntaxError(self.filePath, self, f"Variable '{varName}' already defined.", 0, 0)
        else:
            if constant:
                self.constants[varName] = varValue
            else:
                self.variables[varName] = varValue

        return varValue

    def lookup(self, var:identifierNode) -> None:
        varName = var.symbol
        env = self.resolve(varName)
        if varName in self.constants:
            return env.constants[varName]
        elif varName in self.variables:
            return env.variables[varName]
        else:
            return nameError(self.filePath, self, varName, var.column, var.line)

    def resolve(self, varName: str) -> None:
        if varName in self.variables:
            return self
        elif varName in self.constants:
            return self
        
        if self.parent == None:
            return nameError(self.filePath, self, varName, 0, 0)
        else:
            return self.parent.resolve(varName)

def createGlobalEnvironment(parent=None, filePath:str='') -> environment:
    env = environment(parent, filePath)
    # functions
    env.declareVariable('output', nativeFunction(lambda args, scope : sys.stdout.write(str(bif.output(filePath, args[0])) + '\n')), True)
    env.declareVariable('input', nativeFunction(lambda args, scope : bif.in_(filePath, args[0])), True)
    env.declareVariable('type', nativeFunction(lambda args, scope : bif.type_(filePath, args[0])), True)
    env.declareVariable('hash', nativeFunction(lambda args, scope : bif.hash(filePath, args[0])), True)
    env.declareVariable('Str', nativeFunction(lambda args, scope: bif.hardCastStr(filePath, args[0])), True)
    env.declareVariable('Int', nativeFunction(lambda args, scope: bif.hardCastInt(filePath, args[0])), True)
    env.declareVariable('Real', nativeFunction(lambda args, scope: bif.hardCastReal(filePath, args[0])), True)

    # Move to modules
    env.declareVariable('now', nativeFunction(lambda args, scope : bif.now(filePath, )), True)
    env.declareVariable('wait', nativeFunction(lambda args, scope : bif.wait(filePath, args[0])), True)

    # variables
    env.declareVariable('_', nullValue(), True)
    env.declareVariable('T', booleanValue("T"), True)
    env.declareVariable('F', booleanValue("F"), True)
    
    return env