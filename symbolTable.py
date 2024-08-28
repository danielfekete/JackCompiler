STATIC = "STATIC"
FIELD = "FIELD"
ARG = "ARG"
VAR = "VAR"

class SymbolTable:
    def __init__(self):
        self._classTable={}
        self._subroutineTable={}
        self._index={
            'static':0,
            'field':0,
            'arg':0,
            'var':0
        }
        
    # Starts a new subroutine scope
    def startSubroutine(self):
        self._subroutineTable.clear()
        self._index['argument'] = 0
        self._index['local'] = 0
    # Defines a new identifier of a given name, type, and kind and assigns it a running index
    def define(self,name:str,type:str,kind:str):
        new = (type,kind,self._index[kind])
        if kind in ['static','field']:
            self._classTable[name] = new
        else:
            self._subroutineTable[name] = new
        self._index[kind] += 1
    # Returns the number of variables of the given kind already defined in the current scope
    def varCount(self,kind:str)->int:
        self._index[kind]
    # Returns the kind of the named identifier in the current scope. If the identifier is unknown in the current scope, returns NONE
    def kindOf(self,name:str)->str | None:
        identifier=self._getIdentifier(name)
        if identifier:
            return identifier[1]
        return None
    # Returns the type of the named identifier in the current scope
    def typeOf(self,name:str)->str | None:
        identifier = self._getIdentifier(name)
        if identifier:
            return identifier[0]
        return None
    # Returns the index assigned to the named identifier.
    def indexOf(self,name:str)->int:
        identifier = self._getIdentifier(name)
        if identifier:
            return identifier[2]
        return None
    def _getIdentifier(self,name:str):
        if name in self._subroutineTable:
            return self._subroutineTable[name]
        if name in self._classTable:
            return self._classTable[name]
        return None
    
    # Getters

    def getSubroutineTable(self):
        return self._subroutineTable
    
    def getClassTable(self):
        return self._classTable