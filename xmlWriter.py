import jackTokenizer

class XmlWriter:
    @staticmethod
    def writeToken(token,tokenType) -> str:
        if tokenType == jackTokenizer.INT_CONST:
            return f"<integerConstant> {token} </integerConstant>\n"
        elif tokenType == jackTokenizer.STRING_CONST:
            return f"<stringConstant> {token} </stringConstant>\n"
        elif tokenType == jackTokenizer.KEYWORD:
            return f"<keyword> {token} </keyword>\n"
        elif tokenType == jackTokenizer.SYMBOL:
            if token == '>':
                token = '&gt;'
            elif token == '<':
                token = '&lt;'
            elif token == '"':
                token = '&quot;'
            elif token == '&':
                token = '&amp;'
            return f"<symbol> {token} </symbol>\n"
        else:
            return f"<identifier> {token} </identifier>\n"

    @staticmethod
    def writeStartSegment(segment) -> str:
        return f'<{segment}>\n'

    @staticmethod
    def writeEndSegment(segment) -> str:
        return f'</{segment}>\n'