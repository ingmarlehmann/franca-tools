#------------------------------------------------------------------------------
# fidlparser: fidl_parser.py
#
# FidlParser class: Parser for Franca IDL (*.fidl).
#                   Builds and AST.
# 
# This code is *heavlily* inspired by 'pycparser' by Eli Bendersky 
# (https://github.com/eliben/pycparser/)
#
# Copyright (C) 2016, Ingmar Lehmann
# License: BSD
#------------------------------------------------------------------------------
import sys
from ply import yacc
from franca_lexer import FidlLexer

input_text = '' 
 
for line in sys.stdin: 
    input_text += line 

class FidlParser(object):
    def __init__(self):
        self.lexer = FidlLexer(self.on_lexer_error)
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    def on_lexer_error(self, error):
        print error

    def parse(self, text):
        self.parser.parse(input=text,lexer=self.lexer)

    def p_any(self, p):
        '''any : enumeration 
                | enumeration any
                | method
                | method any'''

        print("found any")
        p[0] = p[1]

    def p_enumeration(self, p):
        'enumeration : ENUMERATION ID LBRACE enumeration_value RBRACE'
        print("found enumeration!")
        p[0] = p[0]

    def p_enumeration_value(self, p):
        '''enumeration_value : ID EQUALS INT_CONST_DEC
                            | ID EQUALS INT_CONST_DEC enumeration_value
                            | ID 
                            | ID enumeration_value
            '''
        print("found enumeration_value")    
        p[0] = p[0]

    def p_typename(self, p):
        '''typename : INT64
                    | INT32
                    | INT16
                    | INT8
                    | INTEGER
                    | UINT64
                    | UINT32
                    | UINT16
                    | UINT8
                    | BOOLEAN
                    | STRING
                    | FLOAT
                    | DOUBLE
                    | BYTEBUFFER
        '''
        print("found typename")
        p[0] = p[0]

    def p_method(self, p):
        '''method : METHOD ID LBRACE method_body RBRACE'''
        print("found method")
        p[0] = p[0]

    def p_method_body(self, p):
        '''method_body : method_in_params
                        | method_out_params
                        | method_in_params method_out_params
                        | method_out_params method_in_params'''
        print("found method_body")                
        p[0] = p[0]

    def p_method_in_params(self, p):
        '''method_in_params : IN LBRACE method_param_list RBRACE'''
        print("found method_in_params")
        p[0] = p[0]

    def p_method_out_params(self, p):
        '''method_out_params : OUT LBRACE method_param_list RBRACE'''
        print("found method_out_params")
        p[0] = p[0]

    def p_method_param_list(self, p):
        '''method_param_list : typename ID 
                                | typename ID method_param_list'''
        print("found method_param_list")                                
        p[0] = p[0]

    def p_error(self, p):
        print("Syntax error in input!" + str(p))

parser = FidlParser()

test_text = """
    enumeration { Int32 a }
    enumeration { Int32 b }
"""

#parser.parse(test_text)
parser.parse(input_text)
