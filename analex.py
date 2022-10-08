
from re import I


ERR = -1
ACP = 999
idx = 0
entrada = ''
matran=[
    #0      1       2   3    4    5    6    7   8   9   10    11   12    13
    #letra  digito  _   .    -    Del  OpA  =   !   <,> DeU   "    /     \n
    [5,     2,      5,  ERR, 1,   12,  11,  8,  9,  6,  0,  13,   15,   0], #0
    [ACP,   2,      ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP, ACP,   ACP], #1 OpA -
    [ACP,   2,      ACP,3,   ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP, ACP,   ACP], #2
    [ERR,   4,      ERR,ERR, ERR, ERR, ERR, ERR,ERR,ERR,ERR,ACP, ERR,   ACP], #3
    [ACP,   4,      ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP, ACP,   ACP], #4
    [5,     5,      5,  ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP, ACP,   ACP], #5
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, 7,  ACP,ACP,ACP,ACP, ACP,   ACP], #6
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP, ACP,   ACP], #7
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, 10, ACP,ACP,ACP,ACP, ACP,   ACP], #8
    [ERR,   ERR,    ERR,ERR, ERR, ERR, ERR, 10, ERR,ERR, ERR,ERR,ERR,   ERR], #9
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP, ACP,   ACP], #10
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP,  16,   ACP], #11  OpA
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP, ACP,   ACP], #12  Del
    [13,    13,      13, 13,  13,  13,  13,  13, 13, 13, 13, 14,  13,   ACP], #13  Del
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP, ACP,   ACP], #14  Del
    
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP,  16,   ACP], #15 OpA
    [16,     16,     16, 16,  16,  16,  16,  16, 16, 16,16, 16,  16,   17],  #16 Comment
    [0,   0,    0,0, 0, 0, 0, 0,0,0,0,0, 0,   0], #17 Aceptador
]
palRes = ['lee', 'imprime', 'imprimenl', 'verdadero', 
          'falso', 'entero', 'logico', 'decimal', 'palabra',
          'desde', 'mientras', 'si', 'sino', 'haz', 
          'hasta', 'que', 'y', 'o', 'no', 'nulo', 'regresa']

def esReservada(lex):
    global palRes
    for x in palRes:
        if x == lex: return True
    
    return False

def error(c, des):
    print(c, des)
    return ERR

def colCar( x ):
    if (ord(x) >= 65 and ord(x) <= 90) or \
       (ord(x) >= 97 and ord(x) <= 122): return 0 
    if (ord(x) >= 48 and ord(x) <= 57): return 1
    if x == '_': return 2
    if x == '.': return 3
    if x == '-': return 4
    if x == '{' or x == '}' or x == '(' or x == ')' or \
       x == '[' or x == ']' or x == ';' or x == ',' or \
       x == ':': return 5  #delimitador
    if x == '+' or x == '*' or \
       x == '^' or x == '%': return 6
    if x == '=': return 7
    if x == '!': return 8
    if x == '<' or x == '>': return 9
    if x == ' ' or x == '\t': return 10
    if x == '"': return 11
    #Comentario
    if x == '/': return 12
    if x == '\n': return 13
    else: return error(x, 'Simbolo Ilegal NO válido en Lenguaje')

def scanner():
    global entrada, ERR, idx, matran
    estado = 0
    lexema = ''
    token = ''
    estAnt = 0
    while estado != ERR and idx < len(entrada):
        c = entrada[idx]
        idx += 1
        col = colCar( c )
        if col >=0 and col <=13:
            estAnt = estado
            if estado != ERR and estado != ACP:
                estado = matran[estado][col]
            #print('lexema=', lexema)
            
            if estado == 15:
                if colCar(entrada[idx]) == 1:
                    estado = 15
                else:
                    estado = 16
                
            if estado != ERR and estado != ACP and col != 10 and col != 13 and estado!= 16 or estado == 13:
                lexema += str(c)
                #print('Estado anterior:',estAnt,'Estado actual:',estado,'Simbolo:',c)
            elif estado == ACP:
                if col != 10:
                    idx -= 1
                break
        else: estado = ERR
        #print(estado,c)
    if estado != ACP and estado != ERR: estAnt = estado
    #Verifica Token
    if estAnt == 2: token='Ent'
    elif estAnt == 3 or estAnt == 9: error(lexema, 'Error Léxico')
    elif estAnt == 4: token = 'Dec'
    elif estAnt == 5:
        token = 'Ide'
        if esReservada(lexema): token = 'Res'
        if lexema == 'y' or lexema == 'o' or \
           lexema == 'no': token = 'OpL'
        elif lexema == 'verdadero' or lexema == 'falso': token='CtL' 
    elif estAnt == 6 or estAnt == 7 or estAnt == 10: token='OpR'
    elif estAnt == 8: token = 'OpS'
    elif estAnt == 1 or estAnt == 11: token = 'OpA'
    elif estAnt == 12: token = 'Del'
    elif estAnt == 14: token = 'Cad'
    # Aki empiezo io
    elif estAnt == 15: token = 'OpA'
    #elif estAnt == 16: token = 'CMM1'
    #elif estAnt == 17: token = 'CMM2'

    return token, lexema
    
if __name__ == '__main__':
    arche = input('Archivo (.icc) [.]=salir: ')
    if arche == '.': exit()
    archivo = open(arche, 'r')
    entrada = ''
    for linea in archivo:
        entrada += linea
    
    print('Token', '\t',  'Lexema')
    print('-----', '\t', '------')
    while entrada != '' and idx < len(entrada):
        #print('entrada=', entrada)
        tok, lex = scanner()
        print(tok,'\t', lex)
