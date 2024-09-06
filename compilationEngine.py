import jackTokenizer
import vmWriter
import symbolTable
from osUtils import osTypes
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

    def __init__(self):
        self._tokenizer = None
        self._writer = None
        
        self._className = ''
        self._labelIndex={
            'while':0,
            'if':0
        }
        # construct with os void return types
        self._returnTypes={}
        self._symbolTable = symbolTable.SymbolTable()

    def setTokenizer(self,tokenizer:jackTokenizer.JackTokenizer):
        self._tokenizer = tokenizer

    def setWriter(self,writer:vmWriter.VmWriter):
        self._writer = writer
        
    def run(self,tokenizer:jackTokenizer.JackTokenizer,writer:vmWriter):
        self.setTokenizer(tokenizer)
        self.setWriter(writer)
        while self._tokenizer.hasMoreTokens():
            self._tokenizer.advance()
            self.compileClass()

    # Compiles a complete class
    def compileClass(self) -> None:
        # class
        self._tokenizer.advance()
        # {class name}
        self._className = self._tokenizer.identifier()
        self._tokenizer.advance()
        # {
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
        kind = self._tokenizer.keyWord()
        self._tokenizer.advance()

        # type keyword(int, string, boolean) | identifier(another class)
        type = self._tokenizer.identifier() if self._tokenizer.tokenType() == jackTokenizer.IDENTIFIER else self._tokenizer.keyWord()
        self._tokenizer.advance()

        # Add declaration to the symbol table
        varName = self._tokenizer.identifier()
        self._symbolTable.define(varName,type,kind)
        # {varName}
        self._tokenizer.advance()

        # compile multiple static | field declarations
        while self._tokenizer.tokenType() == jackTokenizer.SYMBOL and self._tokenizer.symbol() == ',':
            # ,
            self._tokenizer.advance()
            varName = self._tokenizer.identifier()
            # Add declaration to the symbol table
            self._symbolTable.define(varName,type,kind)
            # {varName}
            self._tokenizer.advance()
        # ;
        self._tokenizer.advance()
    # Compiles a complete method, contstructor or a function
    def compileSubroutine(self) -> None:
        # Reset the symbol table subroutine
        self._symbolTable.startSubroutine()
        # constructor | function | method
        keyWord = self._tokenizer.keyWord()
        self._tokenizer.advance()
        # void | type: keyword(int, string, boolean) | identifier(another class)
        returnType = self._tokenizer.identifier() if self._tokenizer.tokenType() == jackTokenizer.IDENTIFIER else self._tokenizer.keyWord()
        self._tokenizer.advance()
        # subroutine name
        subroutineName = self._tokenizer.identifier()
        self._returnTypes[f'{self._className}{subroutineName}'] = returnType
        # {subroutineName}
        self._tokenizer.advance()
        # (
        self._tokenizer.advance()
        # add this to argument 0
        if keyWord == "method":
            self._symbolTable.define("this",self._className,"argument")
        varCount = self.compileParameterList()
        # symbol )
        self._tokenizer.advance()
        # function className.subroutineName n
        self._writer.writeFunction(f'{self._className}.{subroutineName}',varCount)
        # handling base address anchoring
        if keyWord == "constructor":
            # Get the number of fields of the class
            fieldCount = self._symbolTable.varCount('field')
            self._writer.writePush('constant',str(fieldCount))
            # Create free memory for the object
            self._writer.writeCall('Memory.alloc',1)
            # Anchor the base address to this
            self._writer.writePop('pointer',0)
        elif keyWord == "method":
            self._writer.writePush('argument',0)
            self._writer.writePop('pointer',0)
        # {
        self._tokenizer.advance()
        # multiple var declarations
        while self._tokenizer.tokenType() == jackTokenizer.KEYWORD and self._tokenizer.keyWord() == 'var':
            self.compileVarDec()
        # multiple statements
        self.compileStatements() 
        # }
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
        return varCount
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
        # compile different statements while | if | let | do | return
        print(self._tokenizer.keyWord())
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
    # Compiles a do statement
    def compileDo(self) -> None:
        # do
        self._tokenizer.advance()
        # subroutine call -> term
        self.compileTerm()
        # ; 
        self._tokenizer.advance()
        
    # Compiles a let statement
    def compileLet(self) -> None:
        # let
        self._tokenizer.advance()
        # var name -> pop
        varName = self._tokenizer.identifier()
        self._tokenizer.advance()
        kind = self._symbolTable.kindOf(varName)
        index = self._symbolTable.indexOf(varName)
        # array handling
        if self._tokenizer.tokenType() == jackTokenizer.SYMBOL and self._tokenizer.symbol() == '[':
            # [
            self._tokenizer.advance()
            self.compileExpression()
            # ]
            self._tokenizer.advance()
            # handling array access using temp
            self._writer.writePop('temp',0)
            # anchor that
            self._writer.writePop('pointer',1)
            self._writer.writePush('temp',0)
            self._writer.writePop('that',0)
        # =
        self._tokenizer.advance()
        self.compileExpression()
        # ;
        self._tokenizer.advance()
        self._writer.writePop(self._kindToSegment(kind),varName)
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
        # return
        self._tokenizer.advance()
        if not self._tokenizer.symbol() == ';':
            # handle expressions
            self.compileExpression()
        else:
            # handling void methods, functions
            self._writer.writePush('constant',0)   
        # ;
        self._tokenizer.advance()
        # write return
        self._writer.writeReturn()  

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
            self._writer.writePush('constant',num)
            self._tokenizer.advance()
        # Handle string const
        elif tokenType == jackTokenizer.STRING_CONST:
            ch = self._tokenizer.stringVal()
            for character in range(0, len(ch)):
                self._writer.writePush('constant',ord(ch[character]))
                self._writer.writeCall("String.appendChar",2)
            self._tokenizer.advance()
        # Handle keyword
        elif tokenType == jackTokenizer.KEYWORD:
            keyWord = self._tokenizer.keyWord()
            if keyWord in ["null","false"]:
                self._writer.writePush("constant",0)
            elif keyWord in ["true"]:
                # negate 1 -> -1
                self._writer.writePush("constant",1)
                self._writer.writeArithmetic(self.OP["-"])
            # this handling
            elif keyWord == "this":
                # base address of the object
                self._writer.writePush('pointer',0)
            self._tokenizer.advance()
        # Handle identifier
        elif tokenType == jackTokenizer.IDENTIFIER:
            # subroutine | class | var name
            varName = self._tokenizer.identifier()
       
            nextToken = self._lookAhead(1)['token']
            # subroutine | class
            if nextToken in ['(','.']:
             
                subroutineName = ""
                # . | (
                self._tokenizer.advance()
                
                # handle class or var name
                if nextToken == '.':
                    # get variable from symbolTable
                    
                    index = self._symbolTable.indexOf(varName)

                    className = varName
                    # handle var name
                    if index:
                        kind = self._symbolTable.kindOf(varName)
                        # push var to the stack
                        self._writer.writePush(self._kindToSegment(kind),index)
                        # get the variable class
                        type = self._symbolTable.typeOf(varName)
                        className = type

                    # subroutine name
                    self._tokenizer.advance()
                    subroutineName=f'{className}.{self._tokenizer.identifier()}'    
                    
                    # self._tokenizer.advance()
                else:
                    subroutineName = f'{self._className}.{varName}'                
                # (
                self._tokenizer.advance()
                n = self.compileExpressionList()
                # )
                self._tokenizer.advance()
                self._writer.writeCall(subroutineName,n)
        
                # handleReturn type         
                returnType = ""
                if subroutineName in self._returnTypes:
                    returnType = self._returnTypes[subroutineName]
                else:
                    # os functions
                    returnType = osTypes[subroutineName]
                if returnType == "void":
                    # pop temp 0
                    self._writer.writePop('temp',0)
            else:
                kind = self._symbolTable.kindOf(varName)
                index =  self._symbolTable.indexOf(varName)
                self._writer.writePush(self._kindToSegment(kind),index)
                self._tokenizer.advance()
                if nextToken == '[':
                    # handle array indexing
                    # symbol [
                    self._tokenizer.advance()
                    self.compileExpression()
                    # symbol ]
                    self._tokenizer.advance()
                # handling array access
                self._writer.writePush(self._kindToSegment(kind),index)
                self._writer.writeArithmetic('add')
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
        varCount = 0
        while self._tokenizer.symbol() == ',' or not self._tokenizer.symbol() == ')':
            if varCount > 0:
                # ,
                self._tokenizer.advance()
            self.compileExpression()
            varCount += 1
        return varCount
    


    def _lookAhead(self,by:int):
        tokens = self._tokenizer.getTokens()
        currentPosition = self._tokenizer.getCurrentPosition()
        if currentPosition + by < len(tokens):
            return tokens[currentPosition + by]

    def _kindToSegment(self,kind:str):
        if kind == "var":
            return "local"
        elif kind == "arg":
            return "argument"
        elif kind == "field":
            return "this"
        else:
            return "static"
