import re

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
        # Remove all white spaces and comments from the input
        pattern = r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)|\/\/.+|\/[*]{1,2}.+[*]{1}\/'
        self._input= re.sub(pattern,'',self._input)
        self._currentPosition= -1
        self._tokenize()
        print(self._tokens)


    def _tokenize(self):
        tokens = []
        token = ""
        for index in range(len(self._input)):
            tokenType = None
            character = self._input[index]
            newToken = token + character

            # SYMBOL
            if character in self.symbols:
                newToken = character
                tokenType = SYMBOL
            # KEYWORD
            elif newToken in self.keywords:
                tokenType = KEYWORD
            # INT_CONST
            elif re.match(r"^\d+$",token) and re.match(r"\d",character) and not re.match(r"\d",self._input[index+1]):
                tokenType = INT_CONST
            # STRING_CONST
            elif character == '"' and len(token) and token[0] == '"':
                    tokenType = STRING_CONST
                    newToken = token.replace('"','')
            # IDENTIFIER
            elif self._input[index + 1] in self.symbols:
                tokenType = IDENTIFIER

            # if it's a valid token
            if tokenType:
                tokens.append({
                    'token':newToken,
                    'tokenType':tokenType
                })
                token = ""
            else:
                token = newToken
        self._tokens = tokens

        

    ## Check if the input has more tokens
    def hasMoreTokens(self)->bool:
        return self._currentPosition < len(self._tokens) - 1
    
    # Gets to the next token from the input and make it the current token
    def advance(self):
        if self.hasMoreTokens():
            self._currentPosition += 1
    
    # Returns the current type of the current token
    def tokenType(self):
        return self._tokens[self._currentPosition].tokenType
    
    # Returns the keyword which is the current token, tokenType === KEYWORD
    def keyWord(self)->str:
        if self.tokenType() == KEYWORD:
            return self._tokens[self._currentPosition]
    
    # Returns the character which is the current token, tokenType === SYMBOL
    def symbol(self)->str:
        if self.tokenType() == SYMBOL:
            return self._tokens[self._currentPosition]
    
    # Returns the indentifier which is the current token, tokenType === IDENTIFIER
    def indentifier(self)->str:
        if self.tokenType() == IDENTIFIER:
            return self._tokens[self._currentPosition]
    
    # Returns the integer value of the current token, tokenType === INT_CONST
    def intVal(self)->int:
        if self.tokenType() == INT_CONST:
            return int(self._tokens[self._currentPosition])
    
    # Returns the string value of the current token, tokenType === STRING_CONST
    def stringVal(self)->str:
        if self.tokenType() == STRING_CONST:
            return self._tokens[self._currentPosition]
    
