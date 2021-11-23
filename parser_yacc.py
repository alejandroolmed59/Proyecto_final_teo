import ply.yacc as yacc
from lexer import tokens, lexer

success = True

# Parsing rules
precedence = (
    ("right", "ASSIGN"),
    ("left", "AND", "OR"),
    ("left", "LESS", "GREATER", "EQUALS"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
)

start = "program"


def p_program(p):
    """
    program : function program
            | external-declaration program
            | empty
    """


def p_external_declaration(p):
    """
    external-declaration : type assignment SEMICOLON
                         | array_usage SEMICOLON
                         | type array_usage SEMICOLON
                         | macro_definition
                         | file_inclusion
    """


def p_declaration(p):
    """
    declaration : type assignment SEMICOLON
                | assignment SEMICOLON
                | function_call SEMICOLON
                | array_usage SEMICOLON
                | type array_usage SEMICOLON
    """


def p_assignment(p):
    """
    assignment : ID ASSIGN assignment
               | ID ASSIGN function_call
               | ID ASSIGN array_usage
               | array_usage ASSIGN assignment
               | ID COMMA assignment
               | NUMBER COMMA assignment
               | ID PLUS assignment
               | ID MINUS assignment
               | ID TIMES assignment
               | ID DIVIDE assignment
               | ID MODULUS assignment
               | NUMBER PLUS assignment
               | NUMBER MINUS assignment
               | NUMBER TIMES assignment
               | NUMBER DIVIDE assignment
               | NUMBER MODULUS assignment
               | APOST assignment APOST
               | LPAREN assignment RPAREN
               | MINUS assignment
               | NUMBER PLUS PLUS
               | ID PLUS PLUS
               | array_usage PLUS PLUS
               | NUMBER MINUS MINUS
               | ID MINUS MINUS
               | array_usage MINUS MINUS
               | NUMBER
               | ID
               | LETTER
    """


def p_function_call(p):
    """
    function_call : ID LPAREN RPAREN
                  | ID LPAREN assignment RPAREN
    """


def p_array_usage(p):
    """
    array_usage : ID LBRACKET assignment RBRACKET
    """


def p_function(p):
    """
    function : type ID LPAREN argument_list_option RPAREN compound_statement

    argument_list_option : argument_list
                         | empty

    argument_list : argument_list COMMA argument
                  | argument

    argument : type ID

    compound_statement : LBRACE statement_list RBRACE

    statement_list : statement_list statement
                   | empty

    statement : iteration_statement
              | declaration
              | selection_statement
              | return-statement
    """


def p_type(p):
    """
    type : INT
         | FLOAT
         | CHAR
         | VOID
    """


def p_iteration_statement(p):
    """
    iteration_statement : WHILE LPAREN expression RPAREN compound_statement
                        | WHILE LPAREN expression RPAREN statement
                        | DO compound_statement WHILE LPAREN expression RPAREN SEMICOLON
                        | DO statement WHILE LPAREN expression RPAREN SEMICOLON
    """


def p_selection_statement(p):
    """
    selection_statement : IF LPAREN expression RPAREN compound_statement
                        | IF LPAREN expression RPAREN statement
                        | IF LPAREN expression RPAREN compound_statement ELSE compound_statement
                        | IF LPAREN expression RPAREN compound_statement ELSE statement
                        | IF LPAREN expression RPAREN statement ELSE compound_statement
                        | IF LPAREN expression RPAREN statement ELSE statement
    """


def p_return_statement(p):
    """
    return-statement : RETURN SEMICOLON
                     | RETURN expression SEMICOLON
    """


def p_expression(p):
    """
    expression : expression EQUALS expression
               | expression LESS expression
               | expression GREATER expression
               | expression AND expression
               | expression OR expression
               | NOT expression
               | assignment
               | array_usage
    """


def p_macro_definition(p):
    """
    macro_definition : POUND DEFINE ID assignment
    """


def p_file_inclusion(p):
    """
    file_inclusion : POUND INCLUDE LESS HEADER GREATER
                   | POUND INCLUDE QUOTE HEADER QUOTE
    """


# Handle empty productions
def p_empty(p):
    "empty :"
    pass


# Error rule for syntax errors
def p_error(p):
    global success
    if p:
        print("Syntax error near '%s', line '%s'" % (p.value, p.lineno - 1))
    success = False


# Build the parser
parser = yacc.yacc()


source_code = """
# include <stdlib.h>
# define TRUE 1

// comment

int main (int a) {
    if (a =  2) {

    }
}
"""

# Give the lexer some input
lexer.input(source_code)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)

print("\n")

lexer.lineno = 0

# Parse
parser.parse(source_code)

# Print result
if success:
    print("Input is valid")
else:
    print("Input is not valid")
