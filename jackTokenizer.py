import re
import xmlWriter

SYMBOL = "SYMBOL"
KEYWORD = "KEYWORD"
IDENTIFIER = "IDENTIFIER"
STRING_CONST = "STRING_CONST"
INT_CONST = "INT_CONST"

class JackTokenizer:
    
    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean','void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']

    symbols = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']

    def __init__(self,src:str):
        # Open the input file
        with open(src,'r') as file:
            self._input=file.read()
        # Remove all comments from the input
        commentPattern = r'\/\/.+|\/\*{1,2}[\S\s]*?\*\/'
        self._input= re.sub(commentPattern,'',self._input).strip()
        self._currentPosition= -1
        self._currentToken= ""
        self._tokens=[]
        self._out=""
        self._tokenize()


    def _tokenize(self):
        tokens = []
        
        self._appendOut(xmlWriter.XmlWriter.writeStartSegment('tokens'))
        # Split by white spaces except white spaces between double qoutes
        for part in re.split(r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)',self._input):
            token = ""
            partLen=len(part)
            # Loop through the characters one by one
            for index in range(partLen):
                tokenType = None
                character = part[index]
                newToken = token + character

                # SYMBOL
                if character in self.symbols:
                    newToken = character
                    tokenType = SYMBOL
                # KEYWORD
                elif newToken in self.keywords:
                    tokenType = KEYWORD
                # INT_CONST
                elif re.match(r"^\d*$",token) and re.match(r"\d",character) and (index == partLen - 1 or not re.match(r"\d",part[index+1])):
                    tokenType = INT_CONST
                # STRING_CONST
                elif character == '"' and len(token) and token[0] == '"':
                        tokenType = STRING_CONST
                        newToken = token.replace('"','')
                # IDENTIFIER
                elif index == partLen - 1 or part[index + 1] in self.symbols:
                    tokenType = IDENTIFIER

                # if it's a valid token
                if tokenType:
                    tokens.append({
                        'token':newToken,
                        'tokenType':tokenType
                    })
                    # Write token to output xml
                    self._appendOut(xmlWriter.XmlWriter.writeToken(newToken,tokenType))
                    token = ""
                else:
                    token = newToken
        self._appendOut(xmlWriter.XmlWriter.writeEndSegment('tokens'))
        self._tokens = tokens

        

    ## Check if the input has more tokens
    def hasMoreTokens(self)->bool:
        return self._currentPosition < len(self._tokens) - 1
    
    # Gets to the next token from the input and make it the current token
    def advance(self):
        if self.hasMoreTokens():
            self._currentPosition += 1
            self._currentToken = self._tokens[self._currentPosition]
    
    # Returns the current type of the current token
    def tokenType(self):
        return self._currentToken['tokenType']
    
    # Returns the keyword which is the current token, tokenType === KEYWORD
    def keyWord(self)->str:
        if self.tokenType() == KEYWORD:
            return self._currentToken['token']
    
    # Returns the character which is the current token, tokenType === SYMBOL
    def symbol(self)->str:
        if self.tokenType() == SYMBOL:
            return self._currentToken['token']
    
    # Returns the indentifier which is the current token, tokenType === IDENTIFIER
    def indentifier(self)->str:
        if self.tokenType() == IDENTIFIER:
            return self._currentToken['token']
    
    # Returns the integer value of the current token, tokenType === INT_CONST
    def intVal(self)->int:
        if self.tokenType() == INT_CONST:
            return int(self._currentToken['token'])
    
    # Returns the string value of the current token, tokenType === STRING_CONST
    def stringVal(self)->str:
        if self.tokenType() == STRING_CONST:
            return self._currentToken['token']

    def _appendOut(self,app):
        self._out += app
    
    # Getters
    def getCurrentPosition(self)->int:
        return self._currentPosition
    def getCurrentToken(self):
        return self._currentToken
    def getTokens(self):
        return self._tokens
    def getOut(self):
        return self._out
