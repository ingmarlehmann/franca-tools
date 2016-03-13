import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from franca_parser import franca_lexer

input_text = ''

for line in sys.stdin:
    input_text += line

class FrancaLexerDebugPrinter(object):
    def __init__(self):
        self.franca_lexer = franca_lexer.FrancaLexer(self.on_error)
        self.franca_lexer.build()
        self.tokens = self.franca_lexer.tokens

    def input(self, text):
        self.franca_lexer.input(text)

    def token(self):
        return self.franca_lexer.token()
    
    def on_error(self, error):
        print "error: " + error
    
    def print_tokens(self):
        while True:
            tok = self.token()
            if not tok:
                break # no more input
            print tok

lexer_printer = FrancaLexerDebugPrinter()
lexer_printer.input(input_text)
lexer_printer.print_tokens()
