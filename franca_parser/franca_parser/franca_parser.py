#------------------------------------------------------------------------------
# franca_parser: franca_parser.py
#
# FrancaParser class: Parser for Franca IDL (*.fidl).
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
from franca_lexer import FrancaLexer

class FrancaParser(object):
    def __init__(self):
        self.lexer = FrancaLexer(self.on_lexer_error)
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    def on_lexer_error(self, error):
        print error

    def parse(self, text):
        return self.parser.parse(input=text,lexer=self.lexer)

    def p_document(self, p):
        '''document : package_statement import_statement_list root_level_object_list
                    | package_statement root_level_object_list'''
        p[0] = p[0]

    def p_document_root_level_object_list(self, p):
        '''root_level_object_list : root_level_object 
                                | root_level_object root_level_object_list'''
        p[0] = p[0]

    def p_root_level_object(self, p):
        '''root_level_object : interface
                            | type_collection'''
        p[0] = p[0]
   
    def p_import_statement_list(self, p):
        '''import_statement_list : import_statement
                                | import_statement import_statement_list'''
        p[0] = p[0]

    def p_import_statement(self, p):
        '''import_statement : IMPORT import_identifier FROM string'''
        p[0] = p[0]

    def p_interface(self, p):
        '''interface : INTERFACE identifier LBRACE complex_type_declaration_list RBRACE
                        | franca_comment INTERFACE identifier LBRACE complex_type_declaration_list RBRACE'''
        if len(p) == 6:
            p[0] = franca_ast.Interface(p[2], p[4], None)
        else:
            p[0] = franca_ast.Interface(p[3], p[5], p[1])
        
        p[0].show()

    def p_type_collection(self, p):
        '''type_collection : TYPECOLLECTION identifier LBRACE complex_type_declaration_list RBRACE
                        | franca_comment TYPECOLLECTION identifier LBRACE complex_type_declaration_list RBRACE'''
        if len(p) == 6:
            p[0] = franca_ast.TypeCollection(p[2], p[4], None)
        else:
            p[0] = franca_ast.TypeCollection(p[3], p[5], p[1])

        p[0].show()
    
    def p_complex_type_declaration_list(self, p):
        '''complex_type_declaration_list : complex_type_declaration
                                        | complex_type_declaration complex_type_declaration_list'''
        if len(p) == 2:
            p[0] = franca_ast.ComplexTypeDeclarationList([p[1]])
        else:
            p[2].members.append(p[1])
            p[0] = p[2]

    def p_complex_type_declaration(self, p):
        '''complex_type_declaration : enumeration_declaration 
                                    | struct_declaration
                                    | map_declaration
                                    | union_declaration
                                    | method_declaration
                                    | attribute_declaration
                                    | version_declaration
                                    | explicit_array_type_declaration
                                    | typedef'''
        p[0] = p[1]

    def p_attribute_declaration(self, p): # TODO: readonly, noSubscriptions
        '''attribute_declaration : ATTRIBUTE typename identifier'''
        p[0] = franca_ast.Attribute(p[2], p[3])

    def p_explicit_array_declaration(self, p): # todo, support multiple dimensions (array of array type)
        '''explicit_array_type_declaration : ARRAY identifier OF typename'''
        p[0] = franca_ast.ArrayTypeDeclaration(p[2], p[4], 1)

    def p_implicit_array_declaration(self, p):
        '''implicit_array_type_declaration : typename LBRACKET RBRACKET'''
        p[0] = franca_ast.ArrayTypeDeclaration(None, p[1], 1)

    def p_map_declaration(self, p):
        '''map_declaration : MAP identifier LBRACE typename TO typename RBRACE
                | franca_comment MAP identifier LBRACE typename TO typename RBRACE'''
        if len(p) == 8:
            p[0] = franca_ast.Map(p[2], p[4], p[6], None)
        else:
            p[0] = franca_ast.Map(p[3], p[5], p[7], p[1])

    def p_union_declaration(self, p): # TODO: union inheritance
        '''union_declaration : UNION identifier LBRACE variable_declaration_list RBRACE
                | franca_comment UNION identifier LBRACE variable_declaration_list RBRACE'''
        if len(p) == 6:
            p[0] = franca_ast.Union(p[2], p[4], None)
        else: 
            p[0] = franca_ast.Union(p[3], p[5], p[1])

    def p_struct_declaration(self, p): # TODO: polymorphic structs, struct inheritance
        '''struct_declaration : STRUCT identifier LBRACE variable_declaration_list RBRACE
                    | franca_comment STRUCT identifier LBRACE variable_declaration_list RBRACE'''
        if len(p) == 6:
            p[0] = franca_ast.Struct(p[2], p[4], None)
        elif len(p) == 7:
            p[0] = franca_ast.Struct(p[3], p[5], p[1])

    def p_variable_declaration_list(self, p):
        '''variable_declaration_list : variable_declaration
                                    | variable_declaration variable_declaration_list'''
        if len(p) == 2:
            p[0] = franca_ast.VariableList([p[1]])
        else:
            p[2].members.append(p[1])
            p[0] = p[2]

    def p_variable_declaration(self, p): 
        '''variable_declaration : typename identifier
                                | franca_comment typename identifier'''
        if len(p) == 3:
            p[0] = franca_ast.Variable(p[1], p[2], None)
        else:
            p[0] = franca_ast.Variable(p[2], p[3], p[1])
    
    def p_enumeration_declaration(self, p): # TODO: enumeration inheritance
        '''enumeration_declaration : ENUMERATION identifier LBRACE enumeration_member_declaration_list RBRACE
                        | franca_comment ENUMERATION identifier LBRACE enumeration_member_declaration_list RBRACE'''
        if len(p) == 6:
            p[0] = franca_ast.Enum(p[2], p[4], None)
        elif len(p) == 7:
            p[0] = franca_ast.Enum(p[3], p[5], p[1])

    def p_enumeration_value_list(self, p):
        '''enumeration_member_declaration_list : enumeration_member_declaration
                                                | enumeration_member_declaration enumeration_member_declaration_list'''
        if len(p) == 2:
            p[0] = franca_ast.EnumeratorList([p[1]])
        elif len(p) == 3:
            p[2].enumerators.append(p[1])
            p[0] = p[2]

    # TODO: Handle expressions in assignment of enum value
    def p_enumeration_member_declaration(self, p):
        '''enumeration_member_declaration : identifier EQUALS const_int
                            | identifier EQUALS string
                            | franca_comment identifier EQUALS const_int
                            | franca_comment identifier EQUALS string
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

    def p_method_declaration(self, p): # TODO: error{} declarations, error inheritance
        '''method_declaration : METHOD identifier LBRACE method_body RBRACE
                            | franca_comment METHOD identifier LBRACE method_body RBRACE'''
        if len(p) == 6:
            p[0] = franca_ast.Method(p[2], None, p[4], False)
        elif len(p) == 7:
            p[0] = franca_ast.Method(p[3], p[1], p[5], False)
    
    def p_fire_and_forget_method_declaration(self, p): 
        '''method_declaration : METHOD identifier FIREANDFORGET LBRACE method_in_arguments RBRACE
                            | franca_comment METHOD identifier FIREANDFORGET LBRACE method_in_arguments RBRACE'''
        if len(p) == 7:
            p[0] = franca_ast.Method(p[2], None, p[5], True)
        elif len(p) == 8:
            p[0] = franca_ast.Method(p[3], p[1], p[6], True)

    def p_broadcast_method_declaration(self, p):
        '''method_declaration : BROADCAST identifier LBRACE method_out_arguments RBRACE
                            | franca_comment BROADCAST identifier LBRACE method_out_arguments RBRACE'''
        if len(p) == 6:
            p[0] = franca_ast.BroadcastMethod(p[2], None, p[4], False)
        elif len(p) == 7:
            p[0] = franca_ast.BroadcastMethod(p[3], p[1], p[5], False)
    
    def p_selective_broadcast_method(self, p):
        '''method_declaration : BROADCAST identifier SELECTIVE LBRACE method_body RBRACE
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

    def p_method_argument(self, p): # TODO: support non POD types (identifier identifier?)
        '''method_argument : typename identifier
                            | franca_comment typename identifier'''
        if len(p) == 3:
            p[0] = franca_ast.MethodArgument(p[1], p[2], None)
        elif len(p) == 4:
            p[0] = franca_ast.MethodArgument(p[2], p[3], p[1])

    def p_typedef(self, p):
        '''typedef : TYPEDEF identifier IS typename'''
        p[0] = franca_ast.Typedef(p[4], p[2])

    def p_typename_1(self, p):
        '''typename : ID'''
        p[0] = franca_ast.Typename(p[1])

    def p_typename_2(self, p):
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
    
    def p_typename_3(self, p):
        '''typename : implicit_array_type_declaration'''
        p[0] = franca_ast.Typename(p[1])
   
    # def p_constant_declarator(self, p):
        # '''constant_declarator : CONST typename EQUALS expression'''
        # p[0] = franca_ast.Constant(p[4])

    # def p_unary_expression(self, p):
        # '''unary_expression : typename PLUS typename
                            # | typename MINUS typename
                            # | typename TIMES typename
                            # | typename DIVIDED typename'''

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

    def p_version_declaration(self, p):
        '''version_declaration : VERSION LBRACE MAJOR const_int MINOR const_int RBRACE'''
        p[0] = franca_ast.Version(p[4], p[6])

    def p_string(self, p):
        '''string : STRING_LITERAL'''
        p[0] = franca_ast.String(p[1])

    def p_integer_constant(self, p):
        '''const_int : INT_CONST_DEC 
                    | INT_CONST_OCT 
                    | INT_CONST_HEX 
                    | INT_CONST_BIN'''
        p[0] = franca_ast.IntegerConstant(p[1])

    # def p_empty(self, p):
        # '''empty : '''

    def p_error(self, p):
        if p is None:
            print "Syntax error: unexpected EOF"
    	else:
            print "Syntax error at line {}: unexpected token {}".format(p.lineno, p.value)

## Debug code used during development ##
## Test by doing 'cat my_interface.fidl | python franca_parser.py'
franca_parser = FrancaParser()

input_text = '' 
for line in sys.stdin: 
    input_text += line 

franca_parser.parse(input_text)
## Debug code used during development ##
