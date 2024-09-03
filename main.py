import sys
import os
import jackAnalyzer
import jackTokenizer
import compilationEngine

def main():
    src = sys.argv[1]

    # Check if the source path exists
    if not os.path.exists(src):
        print('Invalid folder/file path')
        return
    
    jackAnalyzer.JackAnalyzer(src)


    # FIXME: Without the jack analyzer 
    # # Check if the source path is a directory
    # isDir = os.path.isdir(src)

    # if not isDir:
    #     compileFile(src)
    # else:
    #     directory = os.fsencode(src)
    #     # Loop through the jack files inside the directory
    #     for file in os.listdir(directory):
    #         filename = os.fsdecode(file)
    #         if filename.endswith(".jack"):
    #             compileFile(os.path.join(src,filename))




def compileFile(inSrc:str):
    outSrc = inSrc.replace('.jack','.vm')
    # Check if the outfile is already exists
    if os.path.exists(outSrc):
        os.remove(outSrc)
    # Create an outputfile
    outFile = open(outSrc,'w')
    # Create a jack tokenizer
    tokenizer = jackTokenizer.JackTokenizer(inSrc)
    engine = compilationEngine.CompilationEngine(tokenizer)

if __name__ == '__main__':
    main()