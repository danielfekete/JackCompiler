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

        # Tokenize the jack files
        files = []
        tokens = []
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".jack"):
                inSrc = os.path.join(src,filename)
                tokenizer = jackTokenizer.JackTokenizer(inSrc)
                files.append({
                    "path":inSrc,
                    "tokenizer":tokenizer
                })
                # append tokens
                tokens.append(tokenizer.getTokens())
        
        # Set the subroutine table of the jack engine
        engine.setSubroutines(getSubroutines(tokens))

        # Compile the jack files
        for file in files:
            compileFile(file["path"],engine,file["tokenizer"])

def compileFile(inSrc:str,engine:compilationEngine.CompilationEngine,tokenizer:jackTokenizer):
    outSrc = inSrc.replace('.jack','.vm')
    # Check if the outfile is already exists
    if os.path.exists(outSrc):
        os.remove(outSrc)
    
    # Construct a vm writer
    writer = vmWriter.VmWriter(outSrc)
    engine.run(tokenizer,writer)

def getSubroutines(tokens):
    tokensLen = len(tokens)
    subroutines = {}
    for x in range(tokensLen):
        className = ""
        subroutineTokensLen = len(tokens[x])
        for y in range(subroutineTokensLen):
            tokenDict = tokens[x][y]
            token = tokenDict["token"]
            if token in ["class"]:
                className = tokens[x][y+1]["token"]
            elif token in ["function","method","constructor"]:
                kind = token
                returnType = tokens[x][y+1]["token"]
                subroutineName = f'{className}.{tokens[x][y+2]["token"]}'
                subroutines[subroutineName] = {
                    "returnType":returnType,
                    "kind":kind
                }
    return subroutines


if __name__ == '__main__':
    main()