import sys
from franca_lexer import FidlLexer

input_text = ''

for line in sys.stdin:
    input_text += line

class FidlLexerPrinter(object):
    def __init__(self):
        self.fidl_lexer = FidlLexer(self.on_error)
        self.fidl_lexer.build()
        self.tokens = self.fidl_lexer.tokens

    def input(self, text):
        self.fidl_lexer.input(text)

    def token(self):
        return self.fidl_lexer.token()
    
    def on_error(self, error):
        print "error: " + error
    
    def print_tokens(self):
        while True:
            tok = self.token()
            if not tok:
                break # no more input
            print tok

lexer_printer = FidlLexerPrinter()
lexer_printer.input(input_text)
lexer_printer.print_tokens()
