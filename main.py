import sys
import os
import jackTokenizer
import compilationEngine
import vmWriter

def main():
    src = sys.argv[1]

    # Check if the source path exists
    if not os.path.exists(src):
        print('Invalid folder/file path')
        return
    
    # jackAnalyzer.JackAnalyzer(src)

    isDir = os.path.isdir(src)
    engine = compilationEngine.CompilationEngine()

    if not isDir:
        compileFile(src,engine)
    else:
        directory = os.fsencode(src)
        # Loop through the jack files inside the directory
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".jack"):
                compileFile(os.path.join(src,filename),engine)

def compileFile(inSrc:str,engine:compilationEngine.CompilationEngine):
    outSrc = inSrc.replace('.jack','.vm')
    # Check if the outfile is already exists
    if os.path.exists(outSrc):
        os.remove(outSrc)

    # Create a jack tokenizer
    tokenizer = jackTokenizer.JackTokenizer(inSrc)
    writer = vmWriter.VmWriter(outSrc)
    engine.run(tokenizer,writer)

if __name__ == '__main__':
    main()