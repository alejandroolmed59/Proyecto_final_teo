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
    lexer.input(data)
    tok = lexer.token()
    x = stack[-1]  # obtiene el tope de la pila
    while True:
        print("Token tipo:", tok.type)
        print("X:", x )
        print("stack", stack)
        print('\n')
        if x == tok.type and x == "EOF":
            print("Todo bien todo correcto")
            return  # aceptar
        else:
            if x == tok.type and x != "EOF": #Llego a un terminal, llego a una "hoja del arbol"
                symbol_table_insert(tok.value, tok.type, tok.lineno, tok.lexpos) #TODO:DARLE VALOR EN LA TABLA DE SIMBOLO A LOS INDENTIFICADORES
                stack.pop()
                x = stack[-1]
                tok = lexer.token()
                #Se quita el primer elem a la pila y se tiene el siguiente token
            if x in tokens and x != tok.type: #Aparentente es un terminal, pero no es lo que se esperaba
                print("Error: se esperaba ", tok.type)
                print("en la posicion: ", tok.lexpos)
                print("en la linea: ", tok.lineno)
                return 0                                    #TODO: Manejar errores
            if x not in tokens:  # es NO terminal
                celda = buscar_en_tabla(x, tok.type)
                if celda is None: #SI NO hay ninguna produccion
                    print("Error: NO se esperaba", tok.type)
                    print("busco produccion pero no encontró")
                    print("en la posicion: ", tok.lexpos)
                    print("en la linea: ", tok.lineno)
                    return 0                                   #TODO: MANEJAR ERROR
                else:
                    #Vamos bien
                    stack.pop()
                    agregar_pila(celda)
                    x = stack[-1]

        # if not tok:
        # break
        # print(tok)
        # print(tok.type, tok.value, tok.lineno, tok.lexpos)
    

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
 
# Insertar
def symbol_table_insert(name, type, line, pos, valor=""):
    symbol_table[name].append([type, line, pos, valor])

#Actualizar
def symbol_table_updateValue(name,nuevoValor):
    symbol_table[name].valor = nuevoValor;


# Mostrar
def symbol_table_print():
    for variable in symbol_table.items():
        for info in variable:
            print(info)


# Buscar
def symbol_table_search(name):
    print(symbol_table[name])


# Borrar
def symbol_table_delete(name):
    symbol_table.pop(name)


fileData = open("./codigo.c", "r")

miParser(fileData.read()+"$");
#symbol_table_print();
symbol_table_search("b");
