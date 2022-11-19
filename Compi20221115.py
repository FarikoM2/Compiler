ERR = -1
ACP = 999
idx = 0
entrada = ''
noErr = True
arche = ''
archs = ''
nRen=1
nCol=0
pc = 1
ambito = ''

codigo = []
tabSim = []

class oPrgm:
    def __init__(self, nomb, clas, tipo, dim1, dim2):
        self.nomb = nomb
        self.clas = clas
        self.tipo = tipo
        self.dim1 = dim1
        self.dim2 = dim2

def genOprgm(nomb, clas, tipo, dim1, dim2):
    global oPrgm, tamSim
    v = oPrgm(nomb, clas, tipo, dim1, dim2)
    tabSim.append(v)


class code:
    def __init__(self, nemo, dir1, dir2):
        self.nemo = nemo
        self.dir1 = dir1
        self.dir2 = dir2

def genCod(nemo, dir1, dir2):
    global code, codigo
    x = code(nemo, dir1, dir2)
    codigo.append(x)
    
    
# Lexico
matran=[
    #0      1       2   3    4    5    6    7   8   9   10  11  12
    #letra  digito  _   .    -    Del  OpA  =   !   <,> DeU "   /
    [5,     2,      5,  ERR, 1,   12,  11,  8,  9,  6,  0,  13, 15], #0
    [ACP,   2,      ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #1 OpA -
    [ACP,   2,      ACP,3,   ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #2
    [ERR,   4,      ERR,ERR, ERR, ERR, ERR, ERR,ERR,ERR,ERR,ACP], #3
    [ACP,   4,      ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #4
    [5,     5,      5,  ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #5
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, 7,  ACP,ACP,ACP,ACP], #6
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #7
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, 10, ACP,ACP,ACP,ACP], #8
    [ERR,   ERR,    ERR,ERR, ERR, ERR, ERR, 10, ERR,ERR, ERR,ERR], #9
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #10
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #11  OpA
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #12  Del
    [13,    13,     13, 13,  13,  13,  13,  13, 13, 13, 13, 14 ], #13  Del
    [ACP,   ACP,    ACP,ACP, ACP, ACP, ACP, ACP,ACP,ACP,ACP,ACP], #14  Del
]
palRes = ['if', 'else', 'lee', 'imprime', 'imprimenl', 'verdadero', 
          'falso', 'entero', 'logico', 'decimal', 'palabra',
          'desde', 'mientras', 'si', 'sino', 'haz', 
          'hasta', 'que', 'y', 'o', 'no', 'nulo', 'regresa']

def esReservada(lex):
    global palRes
    for x in palRes:
        if x == lex: return True
    
    return False

def error(c, des):
    global ERR, noErr
    cl = nCol - 1
    rn = nRen
    if cl < 1: 
        cl = 1
        rn = nRen - 1
    print('['+str(rn)+', '+str(cl)+ ']', c, des)
    noErr = False
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
    if x == '+' or x == '*' or x == '/' or \
       x == '^' or x == '%': return 6
    if x == '=': return 7
    if x == '!': return 8
    if x == '<' or x == '>': return 9
    if x == ' ' or x == '\t' or x == '\n': return 10
    if x == '"': return 11
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


# Sintactico
def encvarsfuncs():
    global tok, lex, ambito
    if lex != 'nulo' and lex != 'entero' and \
       lex != 'decimal' and lex != 'logico'and \
       lex != 'palabra':
       error('Error de Sintaxis', 'Se esperaba tipo y llegó '+ lex)
    tok, lex = scanner()
    if tok == 'Ide': ambito = lex
    if tok != 'Ide':
            error('Error de Sintaxis', 'Se esperaba <Ide>, y llegó '+ lex)    
    tok, lex = scanner()

def dparams():
    global tok, lex, ambito, pc
    tok, lex = scanner()
    while lex != ')':
        tipo()
        tok, lex = scanner()
        if lex != ',':
            error('Error de Sintaxis', 'Se esperaba <,>, y llegó '+ lex)    
        if tok == 'Ide': 
            ambito = lex
    
def udim(): pass

def dvars():
    global tok, lex, ambito, pc
    tok, lex = scanner()
    tipo()
    tok, lex = scanner()
    if tok != 'Ide':
        error('Error Sintaxis', 'Se esperaba un identificador, y llegó '+ tok)
    tok, lex = scanner()
    if lex == '[':
        udim()
    tok, lex = scanner()
    if lex == '=':
        consts()
     
def tipo():
    global tok, lex, ambito, pc
    tok, lex = scanner()
    if lex != 'nulo' or 'entero' or 'decimal' or 'palabra' or 'logico':
        error('Error Sintaxis', 'Se esperaba tipo, y llegó '+ lex)
        
def consts():
    global tok, lex, ambito, pc
    tok, lex = scanner()
    if tok != 'Ent' or 'CtL' or 'Dec' or 'Cad':
        error('Error Sintaxis', 'Se esperaba constante, y llegó '+ lex) 

def block(): pass

def para(): pass

def mientras(): pass

def hazMientras(): pass

def cte(): 
    if tok == 'Ent' or tok == 'Dec' or tok == 'Cad' or \
       tok == 'Ctl': pass
    else:
        error('Error de Sintaxis', 'se esperaba cte lógica, entera, decimal o cadena y llegó ' + lex)

def termino():
    if lex == '(':
        expr()
        if lex != ')':
           error('Erorr de Sintaxis', 'se esperaba ) y llegó '+lex)
        tok, lex = scanner()
    elif tok == 'Ide':
        tok, lex = scanner()
        if lex == '[': udim()
    else: cte()

def signo(): 
    global tok, lex
    if lex == '-':
        tok, lex = scanner()
    termino()

def expo(): 
    global tok, lex
    opr = '^'
    while opr == '^':
        signo()
        opr = lex
        if opr == '^':
            tok, lex = scanner()

def multi(): 
    global tok, lex
    opr = '*'
    while opr == '*' or opr == '/':
        expo()
        opr = lex
        if opr == '*' or opr == '/':
            tok, lex = scanner()

def expr():
    global tok, lex
    opr = '+'
    while opr == '+' or opr == '-':
        multi()
        opr = lex
        if opr == '+' or opr == '-':
            tok, lex = scanner()

def asigna(): 
    global tok, lex
    tok, lex = scanner()
    if lex == '[': udim()
    if lex != '=': 
        error('Error de Sintaxis', 'Se esperaba = y llegó ' + lex)
    tok, lex = scanner()
    expr()
  
def si(): 
    global tok, lex
    tok, lex = scanner()
    if lex != '(': 
        error("Error de Sintaxis", 'se esperaba ( y llegó ' + lex )
    tok, lex = scanner()
    expr()
    if lex != ')':
        error("Error de Sintaxis", 'se esperaba ) y llegó ' + lex )

def comando(): 
    if tok == 'Ide': asigna()
    if lex == 'si': si()

def estatutos(): 
    if lex != ';': comando()
    if lex != ';': 
        error('Error de Sintaxis', 'Se esperaba <;> y llegó '+ lex)
    tok, lex = scanner()
    if lex != '}': estatutos()

def dfunc():
    global tok, lex, ambito, pc
    tok, lex = scanner()
    if lex != ')': dparams()
    tok, lex = scanner()
    if lex != '{':
        error('Error Sintaxis', 'Se esperaba "{", y llegó '+lex)
    tok, lex = scanner()
    if lex != '}': estatutos()
    if lex == '}':
        print('ambito=', ambito)
        if ambito == 'principal': genCod('OPR', '0', '0')
        elif ambito != '': genCod('OPR', '0', '1')
        pc += 1
    else: 
        error('Error de Sintaxis', 'Se espera "}" en función y llegó ' + lex)

def prgm():
    global tok, lex, idx, ambito, pc
    tok, lex = scanner()
    while (lex == 'nulo' or lex == 'entero' or \
          lex == 'decimal' or lex == 'logico'or \
          lex == 'palabra') and \
          idx < len(entrada):
            encvarsfuncs()
            if lex == '(':
                if ambito=='principal':
                   genOprgm('_P', 'I', 'I', str(pc), '0')
                dfunc()
            else: 
                ambito = ''
                dvars()
          
def parser():
    global noErr, arche, codigo, pc, tabSim, archs
    prgm()
    if noErr:
        print('El archivo['+arche+'] Compiló SIN errores')
        #Impresion de Tambim y Codigo PL0
        aSal=''    
        for x in tabSim:
           aSal += x.nomb+',' + x.clas+',' + x.tipo+',' + x.dim1+',' + x.dim2+',#,\n'
        aSal += '@\n'
        cCod = 1
        for x in codigo:
           aSal += str(cCod) + ' ' + x.nemo + ' '+ x.dir1 +', ' + x.dir1 + '\n'
           if cCod == pc: break
        print(aSal)
        with open(archs, 'w') as salida:
            salida.write(aSal)
            salida.close()

if __name__ == '__main__':
    arche = input('Archivo (.icc) [.]=salir: ')
    if arche == '.': exit()
    archivo = open(arche, 'r')
    entrada = ''
    archs = arche[0:len(arche)-3]
    archs += 'eje'

    for linea in archivo:
        entrada += linea
    print(entrada)
    print(archs)
    parser()
