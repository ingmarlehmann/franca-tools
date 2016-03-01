#------------------------------------------------------------------------------
# fidlparser: fidl_lexer.py
#
# FidlLexer class: Lexer for Franca IDL (*.fidl).
# 
# This code is *heavlily* inspired by 'pycparser' by Eli Bendersky 
# (https://github.com/eliben/pycparser/)
#
# Copyright (C) 2016, Ingmar Lehmann
# License: BSD
#------------------------------------------------------------------------------
from ply import lex
from ply.lex import TOKEN

class FidlLexer(object):
        def __init__(self, error_func):
            """ Create a new Lexer.
                error_func:
                    An error function. Will be called with an error
                    message, line and column as arguments, in case of
                    an error during lexing.
            """
            self.error_func = error_func
            self.last_token = None
            self.filename = ''

        def build(self, **kwargs):
            """ Builds the lexer from the specification. Must be
                called after the lexer object is created.
                This method exists separately, because the PLY
                manual warns against calling lex.lex inside
                __init__
            """
            self.lexer = lex.lex(object=self, **kwargs)

        def input(self, text):
            self.lexer.input(text)

        def token(self):
            self.last_token = self.lexer.token()
            return self.last_token


        ##
        ## Reserved keywords
        ##
        keywords = (
            'IMPORT','FROM','VERSION','BROADCAST','SELECTIVE',
            'IN','OUT','MAJOR','MINOR','PACKAGE','METHOD','EXTENDS','POLYMORPHIC', 
            'ENUMERATION','STRUCT','UNION','MAP','TYPECOLLECTION',
            'TYPEDEF','IS','TO','INTERFACE','CONST','ARRAY','OF',
            'INTEGER','UINT64','INT64','TRUE','FALSE',
            'UINT32','INT32','UINT16','INT16','UINT8','INT8',
            'BOOLEAN','FLOAT','DOUBLE','STRING','BYTEBUFFER'
        )

        keyword_map = {}

        for keyword in keywords:
            if keyword == 'TYPECOLLECTION':
                keyword_map['typeCollection'] = keyword
            elif keyword == 'INTEGER':
                keyword_map['Integer'] = keyword
            elif keyword == 'UINT64':
                keyword_map['UInt64'] = keyword
            elif keyword == 'INT64':
                keyword_map['Int64'] = keyword
            elif keyword == 'UINT32':
                keyword_map['UInt32'] = keyword
            elif keyword == 'INT32':
                keyword_map['Int32'] = keyword
            elif keyword == 'UINT16':
                keyword_map['UInt16'] = keyword
            elif keyword == 'INT16':
                keyword_map['Int16'] = keyword
            elif keyword == 'UINT8':
                keyword_map['UInt8'] = keyword
            elif keyword == 'INT8':
                keyword_map['Int8'] = keyword
            elif keyword == 'BOOLEAN':
                keyword_map['Boolean'] = keyword
            elif keyword == 'FLOAT':
                keyword_map['Float'] = keyword
            elif keyword == 'DOUBLE':
                keyword_map['Double'] = keyword
            elif keyword == 'STRING':
                keyword_map['String'] = keyword
            elif keyword == 'BYTEBUFFER':
                keyword_map['ByteBuffer'] = keyword
            else:
                keyword_map[keyword.lower()] = keyword

        ##
        ## All the tokens recognized by the lexer
        ##
        tokens = keywords + (
            # Identifiers
            'ID',

            # Comments
            'C_COMMENT',
            'FRANCA_COMMENT',

            # String literals
            'STRING_LITERAL',
            
            # Constants
            'INT_CONST_DEC', 'INT_CONST_OCT', 'INT_CONST_HEX', 'INT_CONST_BIN',
            'FLOAT_CONST', 'HEX_FLOAT_CONST',

            # Operators
            'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
            'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
            'LOR', 'LAND', 'LNOT',
            'LT', 'LE', 'GT', 'GE', 'EQ', 'NE', 

             # Assignment
            'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL',
            'PLUSEQUAL', 'MINUSEQUAL',
            'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL',
            'OREQUAL',

            # Increment/decrement
            'PLUSPLUS', 'MINUSMINUS',

            # Conditional operator (?)
            'CONDOP',

             # Delimeters
            'LPAREN', 'RPAREN',         # ( )
            'LBRACKET', 'RBRACKET',     # [ ]
            'LBRACE', 'RBRACE',         # { }
            'COMMA', 'PERIOD',          # . ,
            'SEMI', 'COLON',            # ; :
        )
        
        identifier = r'[a-zA-Z_$][0-9a-zA-Z_$]*'

        hex_prefix = '0[xX]'
        hex_digits = '[0-9a-fA-F]+'
        bin_prefix = '0[bB]'
        bin_digits = '[01]+'

        # integer constants (K&R2: A.2.5.1)
        integer_suffix_opt = r'(([uU]ll)|([uU]LL)|(ll[uU]?)|(LL[uU]?)|([uU][lL])|([lL][uU]?)|[uU])?'
        decimal_constant = '(0'+integer_suffix_opt+')|([1-9][0-9]*'+integer_suffix_opt+')'
        octal_constant = '0[0-7]*'+integer_suffix_opt
        hex_constant = hex_prefix+hex_digits+integer_suffix_opt
        bin_constant = bin_prefix+bin_digits+integer_suffix_opt

        # floating constants (K&R2: A.2.5.3)
        exponent_part = r"""([eE][-+]?[0-9]+)"""
        fractional_constant = r"""([0-9]*\.[0-9]+)|([0-9]+\.)"""
        floating_constant = '(((('+fractional_constant+')'+exponent_part+'?)|([0-9]+'+exponent_part+'))[FfLl]?)'
        binary_exponent_part = r'''([pP][+-]?[0-9]+)'''
        hex_fractional_constant = '((('+hex_digits+r""")?\."""+hex_digits+')|('+hex_digits+r"""\.))"""
        hex_floating_constant = '('+hex_prefix+'('+hex_digits+'|'+hex_fractional_constant+')'+binary_exponent_part+'[FfLl]?)'

        # character constants (K&R2: A.2.5.2)
        # Note: a-zA-Z and '.-~^_!=&;,' are allowed as escape chars to support #line
        # directives with Windows paths as filenames (..\..\dir\file)
        # For the same reason, decimal_escape allows all digit sequences. We want to
        # parse all correct code, even if it means to sometimes parse incorrect
        # code.
        #
        simple_escape = r"""([a-zA-Z._~!=&\^\-\\?'"])"""
        decimal_escape = r"""(\d+)"""
        hex_escape = r"""(x[0-9a-fA-F]+)"""
        #bad_escape = r"""([\\][^a-zA-Z._~^!=&\^\-\\?'"x0-7])"""

        escape_sequence = r"""(\\("""+simple_escape+'|'+decimal_escape+'|'+hex_escape+'))'

        # string literals (K&R2: A.2.6)
        string_char = r"""([^"\\\n]|"""+escape_sequence+')'
        string_literal = '"'+string_char+'*"'
        #bad_string_literal = '"'+string_char+'*'+bad_escape+string_char+'*"'

        #t_ignore = r'\s'
       
        t_STRING_LITERAL = string_literal 
      
        def t_C_COMMENT(self, t):
            r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)' # C and C++ style comments, single and multi line.
            pass # discard c and c++ style comments

        t_FRANCA_COMMENT = r'\<\*{2,}([^*]|[\r\n]|(\*+([^*\>]|[\r\n])))*\*{2,}\>'
        
        def t_NEWLINE(self,t):
            r'\n+'
            t.lexer.lineno += t.value.count("\n")

        # Operators
        t_PLUS              = r'\+'
        t_MINUS             = r'-'
        t_TIMES             = r'\*'
        t_DIVIDE            = r'/'
        t_MOD               = r'%'
        t_OR                = r'\|'
        t_AND               = r'&'
        t_NOT               = r'~'
        t_XOR               = r'\^'
        t_LSHIFT            = r'<<'
        t_RSHIFT            = r'>>'
        t_LOR               = r'\|\|'
        t_LAND              = r'&&'
        t_LNOT              = r'!'
        t_LT                = r'<'
        t_GT                = r'>'
        t_LE                = r'<='
        t_GE                = r'>='
        t_EQ                = r'=='
        t_NE                = r'!='
               
        # Assignment operators
        t_EQUALS            = r'='
        t_TIMESEQUAL        = r'\*='
        t_DIVEQUAL          = r'/='
        t_MODEQUAL          = r'%='
        t_PLUSEQUAL         = r'\+='
        t_MINUSEQUAL        = r'-='
        t_LSHIFTEQUAL       = r'<<='
        t_RSHIFTEQUAL       = r'>>='
        t_ANDEQUAL          = r'&='
        t_OREQUAL           = r'\|='
        t_XOREQUAL          = r'\^=' 

        # Increment/decrement
        t_PLUSPLUS          = r'\+\+'
        t_MINUSMINUS        = r'--'

        # Conditional operator (?)
        t_CONDOP            = r'\?'

        # Delimeters
        t_LBRACE            = r'\{'
        t_RBRACE            = r'\}'
        t_LPAREN            = r'\('
        t_RPAREN            = r'\)'
        t_LBRACKET          = r'\['
        t_RBRACKET          = r'\]'
        t_COMMA             = r','
        t_PERIOD            = r'\.'
        t_SEMI              = r';'
        t_COLON             = r':'
       
        # The following floating and integer constants are defined as
        # functions to impose a strict order (otherwise, decimal
        # is placed before the others because its regex is longer,
        # and this is bad)
        #
        @TOKEN(floating_constant)
        def t_FLOAT_CONST(self, t):
            return t

        @TOKEN(hex_floating_constant)
        def t_HEX_FLOAT_CONST(self, t):
            return t

        @TOKEN(hex_constant)
        def t_INT_CONST_HEX(self, t):
            return t

        @TOKEN(bin_constant)
        def t_INT_CONST_BIN(self, t):
            return t

        @TOKEN(octal_constant)
        def t_INT_CONST_OCT(self, t):
            return t

        @TOKEN(decimal_constant)
        def t_INT_CONST_DEC(self, t):
            return t

        @TOKEN(identifier)
        def t_ID(self, t):
            t.type = self.keyword_map.get(t.value, "ID")
            return t

        def t_error(self, t):
            msg = 'Illegal character %s' % repr(t.value[0])
            self.lexer.skip(1)
             
                #self._error(msg, t)
