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

import franca_ast
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

    def p_interface(self, p):
        '''interface : INTERFACE ID LBRACE interface_member_list RBRACE
                        | FRANCA_COMMENT INTERFACE ID LBRACE interface_member_list RBRACE'''
        print("found interface")
        p[0] = p[0]

    def p_interface_member_list(self, p):
        '''interface_member_list : enumeration 
                | enumeration interface_member_list
                | method
                | method interface_member_list'''

        print("found interface")
        p[0] = p[1]

    def p_enumeration(self, p):
        '''enumeration : ENUMERATION ID LBRACE enumeration_value_list RBRACE
                        | FRANCA_COMMENT ENUMERATION ID LBRACE enumeration_value_list RBRACE'''
        print("found enumeration!")
        p[0] = p[0]

    def p_enumeration_value_list(self, p):
        '''enumeration_value_list : enumeration_value
                                | enumeration_value enumeration_value_list'''
            
        print("found enumeration_value_list")    
        p[0] = p[0]

    def p_enumeration_value(self, p):
        '''enumeration_value : ID EQUALS INT_CONST_DEC
                            | FRANCA_COMMENT ID EQUALS INT_CONST_DEC
                            | ID
                            | FRANCA_COMMENT ID'''
        print("found enumeration_value")
        p[0] = p[0]


    def p_method(self, p):
        '''method : METHOD identifier LBRACE method_body RBRACE
                    | FRANCA_COMMENT METHOD ID LBRACE method_body RBRACE'''
        if len(p) == 6:
            p[0] = franca_ast.Method(p[2], p[4])
        elif len(p) == 7:
            p[0] = franca_ast.Method(p[3], p[5])
        else:
            print("method: unhandled argument number: " + str(len(p)))

        #p[0].show()

    def p_method_body(self, p):
        '''method_body : method_in_params
                        | method_out_params
                        | method_in_params method_out_params
                        | method_out_params method_in_params'''
        #print("found method_body")                
        p[0] = p[0]

    def p_method_in_params(self, p):
        '''method_in_params : IN LBRACE method_argument_list RBRACE'''
        #print("found method_in_params" + str(p[3].children()))
        #print("found method_in_params")
        p[0] = p[0]

    def p_method_out_params(self, p):
        '''method_out_params : OUT LBRACE method_argument_list RBRACE'''
        #print("found method_out_params")
        p[0] = p[0]

    def p_method_argument_list(self, p):
        '''method_argument_list : method_argument
                                | method_argument_list method_argument'''
        if len(p) == 3:
            p[1].args.append(p[2])
            p[0] = p[1]
        else:
            p[0] = franca_ast.MethodArgumentList([p[1]])
       
        p[0].show()

    def p_method_argument(self, p):
        '''method_argument : typename identifier'''
        p[0] = franca_ast.MethodArgument(p[1], p[2])

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
        p[0] = franca_ast.Typename(p[1])
    
    def p_identifier(self, p):
        '''identifier : ID'''
        p[0] = franca_ast.ID(p[1])

    def p_error(self, p):
        print("Syntax error in input!" + str(p))

parser = FidlParser()

test_text = """
    enumeration { Int32 a }
    enumeration { Int32 b }
"""

#parser.parse(test_text)
parser.parse(input_text)
