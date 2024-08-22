import os
import jackTokenizer
import compilationEngine

class JackAnalyzer:
    def __init__(self,src:str):
        
        # Parse src
        if os.path.isdir(src):
            # Loop through the jack files
            directory = os.fsencode(src)
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".jack"):
                    self.analyze(os.path.join(src,filename))        
        else:
            self.analyze(src)


    def analyze(self,src:str):
        # Create a JackTokenizer from the input file
        tokenizer = jackTokenizer.JackTokenizer(src)

        # tokensOutName = src.replace(".jack","T.xml")
        # if os.path.exists(tokensOutName):
        #     # Remove the output file
        #     os.remove(tokensOutName)
        # tokensOutFile = open(tokensOutName,"a")
        # tokensOutFile.write(tokenizer.getOut())

        engine = compilationEngine.CompilationEngine(tokenizer)
        # Create an output file, and write the engine output to it
        outName = src.replace(".jack",".xml")
        # Check if the output file is already exists
        if os.path.exists(outName):
            # Remove the output file
            os.remove(outName)
        outFile = open(outName,"a")
        outFile.write(engine.getOut())
