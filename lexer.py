# ------------------------------------------------------------
# Parser for C language subset
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.
tokens = [
    "NUMBER",
    "LETTER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MODULUS",
    "AND",
    "OR",
    "NOT",
    "EQUALS",
    "LESS",
    "GREATER",
    "LPAREN",
    "RPAREN",
    "HEADER",
    "ID",
    "COMMA",
    "SEMICOLON",
    "APOST",
    "QUOTE",
    "LBRACE",
    "RBRACE",
    "LBRACKET",
    "RBRACKET",
    "POUND",
    "COMMENT",
    "COMMENTBLOCK",
    "ASSIGN",
    "EOF",
]

reserved = {
    "int": "INT",
    "char": "CHAR",
    "float": "FLOAT",
    "if": "IF",
    "else": "ELSE",
    "do": "DO",
    "while": "WHILE",
    "return": "RETURN",
    "void": "VOID",
    "define": "DEFINE",
    "include": "INCLUDE",
}

tokens += list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS = r"\+"
t_MINUS = r"\-"
t_TIMES = r"\*"
t_DIVIDE = r"\/"
t_MODULUS = r"\%"
t_AND = r"\&\&"
t_OR = r"\|\|"
t_NOT = r"\!"
t_EQUALS = r"\=\="
t_LESS = r"\<"
t_GREATER = r"\>"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_COMMA = r"\,"
t_SEMICOLON = r"\;"
t_APOST = r"\'"
t_QUOTE = r"\""
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_POUND = r"\#"
t_ASSIGN = r"\="
t_EOF = r"\$"


# A regular expression rule with some action code
def t_COMMENT(t):
    r"\/\/.*"
    pass


def t_COMMENTBLOCK(t):
    r"\/\*(.|\n)*\*\/"
    pass


def t_HEADER(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*\.h"
    return t


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "ID")  # Check for reserved words
    return t


def t_NUMBER(t):
    r"\d+(\.\d+)?"
    t.value = int(t.value)
    return t


def t_LETTER(t):
    r"\'.\'"
    t.value = t.value.replace("'", "")
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = " \t"

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


#def tokenize(data):
  #  lexer.input(data)
