class VmWriter:
    # Creates a new file and prepares it for writing
    def __init__(self,outPath:str):
        self.outFile = open(outPath,'w')
        pass
    # Writes a VM push command
    def writePush(self,segment:str,index:int)->None:
        self.outFile.write(f'push {segment} {str(index)}\n')
        pass
    # Writes a VM pop command
    def writePop(self,segment:str,index:int)->None:
        self.outFile.write(f'pop {segment} {str(index)}\n')
        pass
    # Writes a VM arithmetic-logical command
    def writeArithmetic(self,command:str)->None:
        self.outFile.write(f'{command.lower()}\n')
        pass
    # Writes a VM label command
    def writeLabel(self,label:str)->None:
        self.outFile.write(f'label {label}\n')
        pass
    # Writes a VM goto command
    def writeGoto(self,label:str)->None:
        self.outFile.write(f'goto {label}\n')
        pass
    # Writes a VM if-goto command
    def writeIf(self,label:str)->None:
        self.outFile.write(f'if-goto {label}\n')
        pass
    # Writes a VM call command
    def writeCall(self,name:str,nArgs:int)->None:
        self.outFile.write(f'call {name} {nArgs}\n')
        pass
    # Writes a VM function command
    def writeFunction(self,name:str,nLocals:int)->None:
        self.outFile.write(f'function {name} {nLocals}')
        pass
    # Writes a VM return command
    def writeReturn(self)->None:
        self.outFile.write('return\n')
        pass
    # Closes the output file
    def close(self)->None:
        self.outFile.close()
        pass