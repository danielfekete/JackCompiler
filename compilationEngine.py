import jackTokenizer
import vmWriter
import symbolTable
class CompilationEngine:
    
    OP = {
        '+':'add',
        '-':'sub',
        '*':'multiply',
        '/':'divide',
        '&':'and',
        '|':'or',
        '<':'lt',
        '>':'gt',
        '=':'eq'
    }
#     ADD,
# SUB, NEG, EQ, GT,
# LT, AND, OR, NOT
# call Math.multiply 2
# call Math.divide 2
    UNARY_OP = {
        '-':'neg',
        '~':'not'
    }

    def __init__(self,tokenizer:jackTokenizer.JackTokenizer,writer:vmWriter.VmWriter):
        self._tokenizer = tokenizer
        self._writer = writer
        self._out = ''
        self._className = ''
        self._labelIndex={
            'while':0,
            'if':0
        }
        self._symbolTable = symbolTable.SymbolTable()
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            self.compileClass()
    # Compiles a complete class
    def compileClass(self) -> None:
        # keyword
        self._tokenizer.advance()
        # class name
        self._className = self._tokenizer.identifier()
        self._tokenizer.advance()
        # symbol
        self._tokenizer.advance()

        # class var declarations, possibly empty
        while self._tokenizer.tokenType() == jackTokenizer.KEYWORD and self._tokenizer.keyWord() in ['static','field']:
            self.compileClassVarDec()

        # class subroutines, possibly empty
        while self._tokenizer.tokenType() == jackTokenizer.KEYWORD and self._tokenizer.keyWord() in ['constructor','function','method']:
            self.compileSubroutine()
        # symbol
        self._tokenizer.advance()
        
    # Compiles a static declaration or a field declaration
    def compileClassVarDec(self) -> None:
        # static | field
        category = self._tokenizer.keyWord()
        self._tokenizer.advance()

        # type keyword(int, string, boolean) | identifier(another class)
        type = self._tokenizer.identifier() if self._tokenizer.tokenType() == jackTokenizer.IDENTIFIER else self._tokenizer.keyWord()
        self._tokenizer.advance()

        # Add declaration to the symbol table
        varName = self._tokenizer.identifier()
        self._symbolTable.define(varName,type,category)
        self._tokenizer.advance()

        # compile multiple static | field declarations
        while self._tokenizer.tokenType() == jackTokenizer.SYMBOL and self._tokenizer.symbol() == ',':
            # symbol ,
            self._tokenizer.advance()
            varName = self._tokenizer.identifier()
            # Add declaration to the symbol table
            self._symbolTable.define(varName,type,category)
            self._tokenizer.advance()
        self._tokenizer.advance()
    # Compiles a complete method, contstructor or a function
    def compileSubroutine(self) -> None:
        # Reset the symbol table subroutine
        self._symbolTable.startSubroutine()
        # constructor | function | method
        keyWord = self._tokenizer.keyWord()
        self._tokenizer.advance()
        # void | type: keyword(int, string, boolean) | identifier(another class)
        type = self._tokenizer.identifier() if self._tokenizer.tokenType() == jackTokenizer.IDENTIFIER else self._tokenizer.keyWord()
        self._tokenizer.advance()
        # subroutine name
        subroutineName = self._tokenizer.identifier()
        self._tokenizer.advance()
        # symbol (
        self._tokenizer.advance()
        # add this to argument 0
        if keyWord == "method":
            self._symbolTable.define("this",self._className,"argument")
        self.compileParameterList()
        # symbol )
        self._tokenizer.advance()
        # symbol {
        self._tokenizer.advance()
        # multiple var declarations
        while self._tokenizer.tokenType() == jackTokenizer.KEYWORD and self._tokenizer.keyWord() == 'var':
            self.compileVarDec()
        # multiple statements
        self.compileStatements() 
        # symbol }
        self._tokenizer.advance()
        
    # Compiles a (possibly empty) parameter list
    def compileParameterList(self) -> None:
        varCount = 0
        # compile multiple parameters
        while self._tokenizer.tokenType() != jackTokenizer.SYMBOL or not self._tokenizer.symbol() == ')':
            if varCount > 0:
                # symbol ,
                self._tokenizer.advance()
            # type
            type = self._tokenizer.identifier() if self._tokenizer.tokenType() == jackTokenizer.IDENTIFIER else self._tokenizer.keyWord()
            self._tokenizer.advance()
            # var name
            varName = self._tokenizer.identifier()
            # add arguments to symbol table
            self._symbolTable.define(varName,type,'argument')
            self._tokenizer.advance()
            varCount += 1
    # Compiles a var declaration
    def compileVarDec(self) -> None:
        # var
        self._tokenizer.advance()
        # type keyword(int, string, boolean) | identifier(another class)
        type = self._tokenizer.identifier() if self._tokenizer.tokenType() == jackTokenizer.IDENTIFIER else self._tokenizer.keyWord()
        self._tokenizer.advance()
        # compile multiple var names
        varName = self._tokenizer.identifier()
        # Add local var declaration
        self._symbolTable.define(varName,type,'local')
        self._tokenizer.advance()

        while self._tokenizer.tokenType() == jackTokenizer.SYMBOL and self._tokenizer.symbol() == ',':
            # symbol ,
            self._tokenizer.advance()
            # Add local var to the symbolTable
            varName = self._tokenizer.identifier()
            self._symbolTable.define(varName,type,'local')
            self._tokenizer.advance()
        # symbol ;
        self._tokenizer.advance()
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
        trueLabel = f'WHILE_END{self._labelIndex['while']}'
        falseLabel = f'WHILE_EXP{self._labelIndex['while']}'
        # Write false label
        self._writer.writeLabel(falseLabel)
        # while
        self._tokenizer.advance()
        # (
        self._tokenizer.advance()
        self.compileExpression()
        # Negate the expression
        self._writer.writeArithmetic('neg')
        # If-goto trueLabel
        self._writer.writeIf(trueLabel)
        # )
        self._tokenizer.advance()
        # {
        self._tokenizer.advance()
        self.compileStatements()
        # }
        self._tokenizer.advance()
        # Goto false label
        self._writer.writeGoto(falseLabel)
        # Write true label
        self._writer.writeLabel(trueLabel)
        self._labelIndex['while'] += 1
        
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
        trueLabel = f'IF_TRUE{str(self._labelIndex['if'])}'
        falseLabel = f'IF_FALSE{str(self._labelIndex['if'])}'

        # if
        self._tokenizer.advance()
        # (
        self._tokenizer.advance()
        self.compileExpression()
        # negate the expression
        self._writer.writeArithmetic('neg')
        # )
        self._tokenizer.advance()
        # If-goto true label
        self._writer.writeIf(trueLabel)
        # {
        self._tokenizer.advance()
        self.compileStatements()
        # }
        self._tokenizer.advance()
        # Goto false label
        self._writer.writeGoto(falseLabel)
        if self._tokenizer.tokenType() == jackTokenizer.KEYWORD:
            keyword = self._tokenizer.keyWord()
            if keyword == 'else':
                # else
                self._tokenizer.advance()
                # {
                self._tokenizer.advance()
                # Write trueLabel
                self._writer.writeLabel(trueLabel)
                self.compileStatements()
                # }
                self._tokenizer.advance()
        # Write falseLabel
        self._writer.writeLabel(falseLabel)
        self._labelIndex['if'] += 1

    # Compiles an expression
    def compileExpression(self) -> None:
        self.compileTerm()
        # Handle op
        symbol = self._tokenizer.symbol()
        while self._tokenizer.tokenType() == jackTokenizer.SYMBOL and symbol in self.OP.keys():
            self._tokenizer.advance()
            self.compileTerm()
            command = self.OP[symbol]
            if symbol in ["*","/"]:
                # call Math function
                self._writer.writeCall(f"Math.{command}",2)
            else:
                self._writer.writeArithmetic(command)
            symbol = self._tokenizer.symbol()
    # Compiles a term
    def compileTerm(self) -> None:
        tokenType = self._tokenizer.tokenType()
        # Handle integer const
        if tokenType == jackTokenizer.INT_CONST:
            num = self._tokenizer.intVal()
            self._writer.writePush('constant',str(num))
            self._tokenizer.advance()
        # Handle string const
        elif tokenType == jackTokenizer.STRING_CONST:
            # TODO: handle string const
            self._tokenizer.advance()
        # Handle keyword
        elif tokenType == jackTokenizer.KEYWORD:
            keyWord = self._tokenizer.keyWord()
            if keyWord in ["null","false"]:
                self._writer.writePush("constant","0")
            elif keyWord in ["true"]:
                # negate 1 -> -1
                self._writer.writePush("constant","1")
                self._writer.writeArithmetic(self.OP["-"])
            self._tokenizer.advance()
        # Handle identifier
        elif tokenType == jackTokenizer.IDENTIFIER:
            nextToken = self._lookAhead(1)['token']
            if nextToken in ['(','.']:
                # handle subroutine call
                self._handleSubroutineCall()
            else:
                # push varName
                varName = self._tokenizer.identifier()
                category = self._symbolTable.kindOf(varName)
                index =  self._symbolTable.indexOf(varName)
                self._writer.writePush(category,index)
                self._tokenizer.advance()
                # TODO: array handling
                if nextToken == '[':
                    # handle array indexing
                    # symbol [
                    self._tokenizer.advance()
                    self.compileExpression()
                    # symbol ]
                    self._tokenizer.advance()
        # Handle symbol
        else:
            symbol = self._tokenizer.symbol()
            # Unary op term
            if symbol in self.UNARY_OP.keys():
                self.compileTerm()
                # Negate, bit wise boolean negate
                self._writer.writeArithmetic(self.UNARY_OP[symbol])
            # Expression in parentheses
            elif symbol == '(':
                # symbol (
                self._tokenizer.advance()
                self.compileExpression()
                # symbol )
                self._tokenizer.advance()
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
