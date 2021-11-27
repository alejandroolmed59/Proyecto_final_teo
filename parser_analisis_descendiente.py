# ------------------------------------------------------------
# Lexer para C
# ------------------------------------------------------------
from lexer import tokens, lexer
from parsing_table import *
from collections import defaultdict

stack = ["EOF", 0]


def miParser(data):
    # f = open('fuente.c','r')
    # lexer.input(f.read())
    ambito = "global"
    lexer.input(data)
    tok = lexer.token()
    x = stack[-1]  # obtiene el tope de la pila
    haveError = False
    while True:
        # print("X:", x)
        # print("stack", stack)
        # print('\n')
        if x == tok.type and x == "EOF":
            if (haveError):
                print("Compilado con errores")
            else:
                symbol_table_print_2()
                print("Todo bien todo correcto")

            return  # aceptar
        else:
            if x == tok.type and x == "IF":
                ambito = "Bloque If"
            if x == tok.type and x == "WHILE":
                ambito = "Bloque while"
            if x == tok.type and x == "RBRACE":
                ambito = "global"
            if x == tok.type and x != "EOF":  # Llego a un terminal, llego a una "hoja del arbol"
                symbol_table_insert_2(tok, ambito)
                symbol_table_insert(tok.value, tok.type, tok.lineno, tok.lexpos)
                stack.pop()
                x = stack[-1]
                tok = lexer.token()
                # Se quita el primer elem a la pila y se tiene el siguiente token
            if x in tokens and x != tok.type:  # Aparentente es un terminal, pero no es lo que se esperaba
                print("Error: se esperaba ", tok.type)
                print("en la posición: ", tok.lexpos)
                print("en la línea: ", tok.lineno)
                haveError = True
                stack.pop()
                if(len(stack) == 0):
                    return 0
                else:
                    x = stack[-1]

            if x not in tokens:  # es NO terminal
                celda = buscar_en_tabla(x, tok.type)
                if celda is None:  # SI NO hay ninguna produccion
                    print("Error: NO se esperaba", tok.type)
                    print("busco producción, pero no encontró")
                    print("en la posición: ", tok.lexpos)
                    print("en la línea: ", tok.lineno)
                    haveError = True
                    stack.pop()
                    if(len(stack) == 0):
                        return 0
                    else:
                        x = stack[-1]
                else:
                    # Vamos bien
                    stack.pop()
                    agregar_pila(celda)
                    x = stack[-1]


def buscar_en_tabla(no_terminal, terminal):
    for i in range(len(tabla2)):
        if tabla2[i][0] == no_terminal and tabla2[i][1] == terminal:
            return tabla2[i][2]  # retorno la celda


def agregar_pila(produccion):
    for elemento in reversed(produccion):
        if elemento != "vacia":  # la vacía no la inserta
            stack.append(elemento)


# Symbol Table
symbol_table = defaultdict(list)
symbol_table_2 = []

def symbol_table_insert_2(lexToken, ambito):
    lexToken.ambito = ambito
    symbol_table_2.append(lexToken)

def symbol_table_print_2():
    for index, lexToken in enumerate(symbol_table_2):
        if (lexToken.type == "ASSIGN"):
            # cad = symbol_table_2[index - 1].value + " = "
            indexCount = index + 1
            while(symbol_table_2[indexCount].type != "SEMICOLON"):
                cad = str(symbol_table_2[indexCount].value) + " "
                indexCount = indexCount + 1
            print("Valor:", cad)
            print("Linea:", symbol_table_2[index - 1].lineno)
            print("Ámbito:", symbol_table_2[index - 1].ambito)
            print('\n')
        else:
            if (lexToken.type != "ID"):
                print("Tipo:", lexToken.type) 
                print("Valor:", "")
                print("Linea:", lexToken.lineno)
                print("Ámbito:", lexToken.ambito)
                print('\n')
            else:
                print("Tipo:", lexToken.type)

# Insertar
def symbol_table_insert(name, type, line, pos, valor=""):
    symbol_table[name].append([type, line, pos, valor])

# Mostrar
def symbol_table_print():
    for variable in symbol_table.items():
        for info in variable:
            print(info)

# Buscar
def symbol_table_search(name):
    print(symbol_table[name])

# Actualizar
def symbol_table_updateValue(name, nuevoValor):
    symbol_table[name].valor = nuevoValor

# Borrar
def symbol_table_delete(name):
    symbol_table.pop(name)


fileData = open("./codigo.c", "r")

miParser(fileData.read()+"$")
# symbol_table_search("b");
# symbol_table_print();
