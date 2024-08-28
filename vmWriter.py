class VmWriter:
    # Creates a new file and prepares it for writing
    def __init__(self) -> None:
        pass
    # Writes a VM push command
    def writePush(self,segment:str,index:int)->None:
        pass
    # Writes a VM pop command
    def writePop(self,segment:str,index:int)->None:
        pass
    # Writes a VM arithmetic-logical command
    def writeArithmetic(self,command:str)->None:
        pass
    # Writes a VM label command
    def writeLabel(self,label:str)->None:
        pass
    # Writes a VM goto command
    def writeGoto(self,label:str)->None:
        pass
    # Writes a VM if-goto command
    def writeIf(self,label:str)->None:
        pass
    # Writes a VM call command
    def writeCall(self,name:str,nArgs:int)->None:
        pass
    # Writes a VM function command
    def writeFunction(self,name:str,nLocals:int)->None:
        pass
    # Writes a VM return command
    def writeReturn(self)->None:
        pass
    # Closes the output file
    def close(self)->None:
        pass