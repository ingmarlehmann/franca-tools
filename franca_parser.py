#------------------------------------------------------------------------------
# fidlparser: fidl_parser.py
#
# FidlParser class: Parser for Franca IDL (*.fidl).
#                   Builds an AST to be used in other tools.
# 
# This code is *heavlily* inspired by 'pycparser' by Eli Bendersky 
# (https://github.com/eliben/pycparser/)
#
# Copyright (C) 2016, Ingmar Lehmann
# License: BSD
#------------------------------------------------------------------------------
import sys
import argparse
import franca_ast

from ply import yacc
from franca_lexer import FidlLexer

class FidlParser(object):
    def __init__(self):
        self.lexer = FidlLexer(self.on_lexer_error)
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    def on_lexer_error(self, error):
        print error

    def parse(self, text):
        return self.parser.parse(input=text,lexer=self.lexer)

    def p_document(self, p):
        '''document : package_statement import_statement_list document_root_object_list
                    | package_statement document_root_object_list'''
        p[0] = p[0]

    def p_document_root_object_list(self, p):
        '''document_root_object_list : document_root_object 
                                    | document_root_object document_root_object_list'''
        p[0] = p[0]

    def p_document_root_object(self, p):
        '''document_root_object : interface''' ## TODO: add typeCollection support
        p[0] = p[0]
   
    def p_import_statement_list(self, p):
        '''import_statement_list : import_statement
                                | import_statement import_statement_list'''
        p[0] = p[0]
    
    def p_import_statement(self, p):
        '''import_statement : IMPORT import_identifier FROM STRING_LITERAL'''
        p[0] = p[0]

    def p_interface(self, p):
        '''interface : INTERFACE identifier LBRACE version interface_member_list RBRACE
                        | franca_comment INTERFACE identifier LBRACE version interface_member_list RBRACE'''
        p[0] = p[0]

    def p_interface_member_list(self, p):
        '''interface_member_list : enumeration 
                | enumeration interface_member_list
                | method
                | method interface_member_list'''

        p[0] = p[1]
        p[0].show()

    def p_enumeration(self, p):
        '''enumeration : ENUMERATION identifier LBRACE enumeration_value_list RBRACE
                        | franca_comment ENUMERATION identifier LBRACE enumeration_value_list RBRACE'''
        if len(p) == 6:
            p[0] = franca_ast.Enum(p[2], p[4], None)
        elif len(p) == 7:
            p[0] = franca_ast.Enum(p[3], p[5], p[1])

    def p_enumeration_value_list(self, p):
        '''enumeration_value_list : enumeration_value
                                | enumeration_value enumeration_value_list'''
            
        if len(p) == 2:
            p[0] = franca_ast.EnumeratorList([p[1]])
        elif len(p) == 3:
            p[2].enumerators.append(p[1])
            p[0] = p[2]

    def p_enumeration_value(self, p):
        '''enumeration_value : identifier EQUALS const_int
                            | franca_comment identifier EQUALS const_int
                            | identifier
                            | franca_comment identifier'''
        if len(p) == 2:
            p[0] = franca_ast.Enumerator(p[1], None, None)
        elif len(p) == 3:
            p[0] = franca_ast.Enumerator(p[2], None, p[1])
        elif len(p) == 4:
            p[0] = franca_ast.Enumerator(p[1], p[3], None)
        elif len(p) == 5:
            p[0] = franca_ast.Enumerator(p[2], p[4], p[1])

    def p_franca_comment(self, p):
        '''franca_comment : FRANCA_COMMENT'''
        p[0] = franca_ast.FrancaComment(p[1])

    def p_method(self, p):
        '''method : METHOD identifier LBRACE method_body RBRACE
                    | franca_comment METHOD identifier LBRACE method_body RBRACE'''
        if len(p) == 6:
            p[0] = franca_ast.Method(p[2], None, p[4], False)
        elif len(p) == 7:
            p[0] = franca_ast.Method(p[3], p[1], p[5], False)
    
    def p_fire_and_forget_method(self, p): 
        '''method : METHOD identifier FIREANDFORGET LBRACE method_in_arguments RBRACE
                    | franca_comment METHOD identifier FIREANDFORGET LBRACE method_in_arguments RBRACE'''
        if len(p) == 7:
            p[0] = franca_ast.Method(p[2], None, p[5], True)
        elif len(p) == 8:
            p[0] = franca_ast.Method(p[3], p[1], p[6], True)

    def p_broadcast_method(self, p):
        '''method : BROADCAST identifier LBRACE method_out_arguments RBRACE
                    | franca_comment BROADCAST identifier LBRACE method_out_arguments RBRACE'''
        if len(p) == 6:
            p[0] = franca_ast.BroadcastMethod(p[2], None, p[4], False)
        elif len(p) == 7:
            p[0] = franca_ast.BroadcastMethod(p[3], p[1], p[5], False)
    
    def p_selective_broadcast_method(self, p):
        '''method : BROADCAST identifier SELECTIVE LBRACE method_body RBRACE
                    | franca_comment BROADCAST identifier SELECTIVE LBRACE method_body RBRACE'''
        if len(p) == 7:
            p[0] = franca_ast.BroadcastMethod(p[2], None, p[5], True)
        elif len(p) == 8:
            p[0] = franca_ast.BroadcastMethod(p[3], p[1], p[6], True)

    def p_method_body_1(self, p):
        '''method_body : method_in_arguments
                        | method_in_arguments method_out_arguments'''
        if len(p) == 2:
            p[0] = franca_ast.MethodBody(p[1], None)
        elif len(p) == 3:    
            p[0] = franca_ast.MethodBody(p[1], p[2])

    def p_method_body_2(self, p):
        '''method_body : method_out_arguments
                        | method_out_arguments method_in_arguments'''
        if len(p) == 2:
            p[0] = franca_ast.MethodBody(None, p[1])
        elif len(p) == 3:    
            p[0] = franca_ast.MethodBody(p[2], p[1])

    def p_method_in_arguments(self, p):
        '''method_in_arguments : IN LBRACE method_argument_list RBRACE'''
        p[0] = franca_ast.MethodInArguments(p[3])

    def p_method_out_arguments(self, p):
        '''method_out_arguments : OUT LBRACE method_argument_list RBRACE'''
        p[0] = franca_ast.MethodOutArguments(p[3])

    def p_method_argument_list(self, p):
        '''method_argument_list : method_argument
                                | method_argument_list method_argument'''
        if len(p) == 3:
            p[1].args.append(p[2])
            p[0] = p[1]
        else:
            p[0] = franca_ast.MethodArgumentList([p[1]])

    def p_method_argument(self, p):
        '''method_argument : typename identifier
                            | franca_comment typename identifier'''
        if len(p) == 3:
            p[0] = franca_ast.MethodArgument(p[1], p[2], None)
        elif len(p) == 4:
            p[0] = franca_ast.MethodArgument(p[2], p[3], p[1])

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
   
    # def p_constant(self, p):
        # '''constant : ID typename EQUALS expression'''
        # p[0] = franca_ast.Constant(p[4])

    def p_identifier(self, p):
        '''identifier : ID'''
        p[0] = franca_ast.ID(p[1])

    def p_import_identifier_1(self, p):
        '''import_identifier : TIMES'''
        p[0] = franca_ast.ImportIdentifier(p[1])

    def p_import_identifier_2(self, p):
        '''import_identifier : ID 
                            | import_identifier PERIOD ID
                            | import_identifier PERIOD TIMES'''
        if len(p) == 4:
            p[1].import_identifier += p[2]
            p[1].import_identifier += p[3]
            p[0] = p[1]
        else:
            p[0] = franca_ast.ImportIdentifier(p[1])
    
    def p_package_statement(self, p):
        '''package_statement : PACKAGE package_identifier'''
        p[0] = franca_ast.PackageStatement(p[2])
    
    def p_package_identifier(self, p):
        '''package_identifier : ID 
                            | package_identifier PERIOD ID'''
        if len(p) == 4:
            p[1].package_identifier += p[2]
            p[1].package_identifier += p[3]
            p[0] = p[1]
        else:
            p[0] = franca_ast.PackageIdentifier(str(p[1]))

    def p_version(self, p):
        '''version : VERSION LBRACE MAJOR const_int MINOR const_int RBRACE'''
        p[0] = franca_ast.Version(p[4], p[6])

    def p_integer_constant(self, p):
        '''const_int : INT_CONST_DEC 
                    | INT_CONST_OCT 
                    | INT_CONST_HEX 
                    | INT_CONST_BIN'''
        p[0] = franca_ast.IntegerConstant(p[1])

    def p_error(self, p):
        print("Syntax error in input!" + str(p))

## Debug code used during development ##
fidl_parser = FidlParser()

input_text = '' 
for line in sys.stdin: 
    input_text += line 

fidl_parser.parse(input_text)
## Debug code used during development ##
