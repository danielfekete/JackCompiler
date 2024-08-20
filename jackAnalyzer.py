import os
import jackTokenizer

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
        jackTokenizer.JackTokenizer(src)