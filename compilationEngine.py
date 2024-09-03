import jackTokenizer
import xmlWriter
import symbolTable
class CompilationEngine:
    OP = ['+','-','*','/','&','|','<','>','=']
    UNARY_OP = ['-','~']

    def __init__(self,tokenizer:jackTokenizer.JackTokenizer):
        self._tokenizer = tokenizer
        self._out=''
        self._symbolTable = symbolTable.SymbolTable()
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            self.compileClass()
    # Compiles a complete class
    def compileClass(self) -> None:
        segment = 'class'
        self._writeStartSegment(segment)
        # keyword
        self._writeToken('class')
        # class name
        classname = self._tokenizer.identifier()
        self._writeIdentifier(classname,'class',True)

        self._writeToken('{')
        # class var declarations, possibly empty
        while self._tokenizer.tokenType() == jackTokenizer.KEYWORD and self._tokenizer.keyWord() in ['static','field']:
            self.compileClassVarDec()
        # class subroutines, possibly empty
        while self._tokenizer.tokenType() == jackTokenizer.KEYWORD and self._tokenizer.keyWord() in ['constructor','function','method']:
            self.compileSubroutine()
        self._writeToken('}')
        self._writeEndSegment(segment)
    # Compiles a static declaration or a field declaration
    def compileClassVarDec(self) -> None:
        segment = 'classVarDec'
        self._writeStartSegment(segment)
        # static | field
        category = self._tokenizer.keyWord()
        self._writeToken(category)
        # type keyword(int, string, boolean) | identifier(another class)
        type = self._tokenizer.identifier() if self._tokenizer.tokenType() == jackTokenizer.IDENTIFIER else self._tokenizer.keyWord()
        self._writeToken(type)
        # var name
        varName = self._tokenizer.identifier()
        # Write the class var declaration
        self._symbolTable.define(varName,type,category)
        self._writeIdentifier(varName,category,True)
        # compile multiple static | field declarations
        while self._tokenizer.tokenType() == jackTokenizer.SYMBOL and self._tokenizer.symbol() == ',':
            self._writeToken(',')
            varName = self._tokenizer.identifier()
            # Write the class var declaration
            self._symbolTable.define(varName,type,category)
            self._writeIdentifier(varName,category,True)
        self._writeToken(';')
        self._writeEndSegment(segment)
    # Compiles a complete method, contstructor or a function
    def compileSubroutine(self) -> None:
        self._symbolTable.startSubroutine()
        segment = 'subroutineDec'
        self._writeStartSegment(segment)
        # constructor | function | method
        self._writeToken(self._tokenizer.keyWord())
        # void | type: keyword(int, string, boolean) | identifier(another class)
        type = self._tokenizer.identifier() if self._tokenizer.tokenType() == jackTokenizer.IDENTIFIER else self._tokenizer.keyWord()
        self._writeToken(type)
        # subroutine name
        subroutineName=self._tokenizer.identifier()
        self._writeIdentifier(subroutineName,'subroutine',True)
        self._writeToken('(')
        self.compileParameterList()
        self._writeToken(')')
        self._writeStartSegment('subroutineBody')
        self._writeToken('{')
        # multiple var declarations
        while self._tokenizer.tokenType() == jackTokenizer.KEYWORD and self._tokenizer.keyWord() == 'var':
            self.compileVarDec()
        # multiple statements
        self.compileStatements() 
        self._writeToken('}')
        self._writeEndSegment('subroutineBody')
        self._writeEndSegment(segment)
    # Compiles a (possibly empty) parameter list
    def compileParameterList(self) -> None:
        segment = 'parameterList'
        self._writeStartSegment(segment)
        varCount = 0
        # compile multiple parameters
        while self._tokenizer.tokenType() != jackTokenizer.SYMBOL or not self._tokenizer.symbol() == ')':
            if varCount > 0:
                self._writeToken(',')
            # type
            type = self._tokenizer.identifier() if self._tokenizer.tokenType() == jackTokenizer.IDENTIFIER else self._tokenizer.keyWord()
            self._writeToken(type)
            # var name
            varName = self._tokenizer.identifier()
            # add arguments to symbol table
            category = 'argument'
            self._symbolTable.define(varName,type,category)
            self._writeIdentifier(varName,category,True)
            varCount += 1
        self._writeEndSegment(segment)
    # Compiles a var declaration
    def compileVarDec(self) -> None:
        segment = 'varDec'
        self._writeStartSegment(segment)
        category = 'var'
        self._writeToken(category)
        # type keyword(int, string, boolean) | identifier(another class)
        type = self._tokenizer.identifier() if self._tokenizer.tokenType() == jackTokenizer.IDENTIFIER else self._tokenizer.keyWord()
        self._writeToken(type)
        # compile multiple var names
        varName = self._tokenizer.identifier()
        # add var declaration, symbol to symboltable
        self._symbolTable.define(varName,type,category)
        self._writeIdentifier(varName,category,True)

        while self._tokenizer.tokenType() == jackTokenizer.SYMBOL and self._tokenizer.symbol() == ',':
            self._writeToken(',')
            varName = self._tokenizer.identifier()
            self._symbolTable.define(varName,type,category)
            self._writeIdentifier(varName,category,True)
        self._writeToken(';')
        self._writeEndSegment(segment)
    # Compiles a sequence of statements
    def compileStatements(self) -> None:
        segment = 'statements'
        self._writeStartSegment(segment)
        # compile different statements while | if | let | do | return
        while self._tokenizer.tokenType() == jackTokenizer.KEYWORD:
            keyword = self._tokenizer.keyWord()
            if keyword == 'while':
                self.compileWhile()
            elif keyword == 'if':
                self.compileIf()
            elif keyword == 'do':
                self.compileDo()
            elif keyword == 'return':
                self.compileReturn()
            else:
                self.compileLet()
        self._writeEndSegment(segment)
    # Compiles a do statement
    def compileDo(self) -> None:
        segment = 'doStatement'
        self._writeStartSegment(segment)
        self._writeToken('do')
        # subroutine call
        self._handleSubroutineCall()
        self._writeToken(';')
        self._writeEndSegment(segment)
    # Compiles a let statement
    def compileLet(self) -> None:
        segment = 'letStatement'
        self._writeStartSegment(segment)
        self._writeToken('let')
        # var name
        varName = self._tokenizer.identifier()
        category = self._symbolTable.kindOf(varName)
        self._writeIdentifier(varName,category,False)
        # array indexing
        if self._tokenizer.tokenType() == jackTokenizer.SYMBOL and self._tokenizer.symbol() == '[':
            self._writeToken('[')
            self.compileExpression()
            self._writeToken(']')
        self._writeToken('=')
        self.compileExpression()
        self._writeToken(';')
        self._writeEndSegment(segment)
    # Compiles a while statement
    def compileWhile(self) -> None:
        segment = 'whileStatement'
        self._writeStartSegment(segment)
        self._writeToken('while')
        self._writeToken('(')
        self.compileExpression()
        self._writeToken(')')
        self._writeToken('{')
        self.compileStatements()
        self._writeToken('}')
        self._writeEndSegment(segment)
    # Compiles a return statement
    def compileReturn(self) -> None:
        segment = 'returnStatement'
        self._writeStartSegment(segment)
        self._writeToken('return')
        # Handle without any expression
        if not self._tokenizer.tokenType() == jackTokenizer.SYMBOL or not self._tokenizer.symbol() == ';':
            self.compileExpression()    
        self._writeToken(';')
        self._writeEndSegment(segment)
    # Compiles an if statement
    def compileIf(self) -> None:
        segment = 'ifStatement'
        self._writeStartSegment(segment)
        self._writeToken('if')
        self._writeToken('(')
        self.compileExpression()
        self._writeToken(')')
        self._writeToken('{')
        self.compileStatements()
        self._writeToken('}')
        if self._tokenizer.tokenType() == jackTokenizer.KEYWORD:
            keyword = self._tokenizer.keyWord()
            if keyword == 'else':
                self._writeToken(keyword)
                self._writeToken('{')
                self.compileStatements()
                self._writeToken('}')
        self._writeEndSegment(segment)
    # Compiles an expression
    def compileExpression(self) -> None:
        segment = 'expression'
        self._writeStartSegment(segment)
        self.compileTerm()
        # Handle op
        symbol = self._tokenizer.symbol()
        while self._tokenizer.tokenType() == jackTokenizer.SYMBOL and symbol in self.OP:
            self._writeToken(symbol)
            self.compileTerm()
            symbol = self._tokenizer.symbol()
        self._writeEndSegment(segment)
    # Compiles a term
    def compileTerm(self) -> None:
        segment = 'term'
        self._writeStartSegment(segment)
        tokenType = self._tokenizer.tokenType()
        # Handle integer const
        if tokenType == jackTokenizer.INT_CONST:
            self._writeToken(self._tokenizer.intVal())
        # Handle string const
        elif tokenType == jackTokenizer.STRING_CONST:
            self._writeToken(self._tokenizer.stringVal())
        # Handle keyword
        elif tokenType == jackTokenizer.KEYWORD:
            self._writeToken(self._tokenizer.keyWord())
        # Handle identifier
        elif tokenType == jackTokenizer.IDENTIFIER:
            nextToken = self._lookAhead(1)['token']
            if nextToken in ['(','.']:
                # handle subroutine call
                self._handleSubroutineCall()
            else:
                varName = self._tokenizer.identifier()
                category = self._symbolTable.kindOf(varName)
                self._writeIdentifier(varName,category,False)
                if nextToken == '[':
                    # handle array indexing
                    self._writeToken('[')
                    self.compileExpression()
                    self._writeToken(']')
        # Handle symbol
        else:
            symbol = self._tokenizer.symbol()
            # Unary op term
            if symbol in ['~','-']:
                self._writeToken(symbol)
                self.compileTerm()
            # Expression in parentheses
            elif symbol == '(':
                self._writeToken(symbol)
                self.compileExpression()
                self._writeToken(')')
        self._writeEndSegment(segment)
    # Compiles a (possibly empty) list of expressions
    def compileExpressionList(self) -> None:
        segment = 'expressionList'
        self._writeStartSegment(segment)
        varCount = 0
        while self._tokenizer.symbol() == ',' or not self._tokenizer.symbol() == ')':
            if varCount > 0:
                self._writeToken(',')
            self.compileExpression()
            varCount += 1
        self._writeEndSegment(segment)

    def getOut(self) -> str:
        return self._out
    def _handleSubroutineCall(self):
        # class name | subroutine name | var name
        varName = self._tokenizer.identifier()
        isClass = self._lookAhead(1)['token'] == '.'
        symbol = self._tokenizer.symbol()
        # handle class or var subroutine
        if isClass:
            self._writeIdentifier(varName, 'class',False)
            self._writeToken(symbol)
            varName = self._tokenizer.identifier()
            self._writeIdentifier(varName,'subroutine',False)
        else:
            category = self._symbolTable.kindOf(varName)
            self._writeIdentifier(varName,category,False)
        self._writeToken('(')
        self.compileExpressionList()
        self._writeToken(')')

    def _lookAhead(self,by:int):
        tokens = self._tokenizer.getTokens()
        currentPosition = self._tokenizer.getCurrentPosition()
        if currentPosition + by < len(tokens):
            return tokens[currentPosition + by]
        
    def _writeToken(self,val:str):
        tokenType=self._tokenizer.tokenType()
        self._appendOut(xmlWriter.XmlWriter.writeToken(val,tokenType))
        self._tokenizer.advance()

    def _writeStartSegment(self,segment):
        self._appendOut(xmlWriter.XmlWriter.writeStartSegment(segment))
    
    def _writeEndSegment(self,segment):
        self._appendOut(xmlWriter.XmlWriter.writeEndSegment(segment))


    def _writeIdentifier(self,name:str,category:str,new:bool):
        segment="identifier"
        self._writeStartSegment(segment)
        # Write the identifier
        self._appendOut(f"<value> {name} </value>\n")
        # Class or subroutine
        if category and category in ['class','subroutine']:
            self._writeCategory(category)
        else:
            # Get the category from the symbolTable and write it
            category = self._symbolTable.kindOf(name)
            # print(f'identifier name: {name}')
            # print(f'category: {category}')
            self._writeCategory(category)
            # write the symbol running index
            self._writeRunningIndex(name)
        # write the smybol status 'declared' | 'used'
        self._writeStatus('declared' if new else 'used')
        self._writeEndSegment(segment)
        self._tokenizer.advance()

    def _writeCategory(self,category):
        self._appendOut(f"<category> {category} </category>\n")

    # Write the running index if the identifier category is var, argument, static or field
    def _writeRunningIndex(self,name:str):
        self._appendOut(f"<index> {str(self._symbolTable.indexOf(name))} </index>\n")

    def _writeStatus(self,status:str):
        self._appendOut(f"<status> {status} </status>\n")

    def _appendOut(self,appendVal):
        self._out+=appendVal
