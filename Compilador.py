import sys
############################################
# DEFININDO AS CLASS - INICO
############################################
class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def setTipo(self, tipo):
        self.tipo = tipo

    def setValor(self, valor):
        self.valor = valor

    def getTipo(self):
        return self.tipo

    def getValor(self):
        return self.valor
############################################
# DEFININDO AS CLASS - FIM
############################################
############################################
# ANALIZADOR LEXICO - INICIO
############################################
# A ANALISE LEXICA FOI CORRETA
LEXICA_CORRETA = True
# LISTA DE TOKENS CRIADOS
TOKENS = []

# TAMANHO MAXIMO TOKENS
MAX_TAMANHO_INTEIRO = 512
MAX_TAMANHO_REAL = 512
MAX_TAMANHO_IDNTIFICADOR = 512
MAX_TAMANHO_STRING = 512

# LISTA DE CARACTER VALIDOS DENTRO DE UM NUMERO
CARACTER_NUMEROS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# LISTA DE CARACTER DO ALFABETO
CARACTER_ALFABETO = ['q', 'Q', 'w', 'W', 'e', 'E', 'r', 'R', 't', 'T', 'y', 'Y', 'u', 'U', 'i', 'I', 'o', 'O', 'p', 'P',
                     'a', 'A', 's', 'S', 'd', 'D', 'f', 'F', 'g', 'G', 'h', 'H', 'j', 'J', 'k', 'K', 'l', 'L', 'z', 'Z',
                     'x', 'X', 'c', 'C', 'v', 'V', 'b', 'B', 'n', 'N', 'm', 'M']
# OPERADORES ALGEBRICOS
OPERADORES_ALGEBRICOS = ['*', '/', '%', '+', '-']
# SEPARADORES MATEMATICOS
SEPARADORES_MATEMATICOS = ['(', ')', '[', ']']
# OPERADORES LOGICOS
OPERADORES_LOGICOS = ['&', '|', '!', '=']
# OUTROS SIMBOLOS
SIMBOLOS_LINGUAGEM = [':', ';', '.']
# CARACTERES IGNORADOS
IGNORE = [9, 32, 10]
#TODAS AS PALAVAS RECERVADAS
PALAVRAS_RESERVADA = ["ATEH","BIT","DE","ENQUANTO","ESCREVA","FIM","FUNCAO","INICIO","INTEIRO","LEIA","NULO","PARA","PARE",
                        "REAL","RECEBA","SE","SENAO","VAR","VET"]
COLUNA = 0
LINHA = 0

# ESTADO INICIAL Q0, ELE E A COMAND ( TEM PRINT )
def q0(texto):
    global COLUNA
    global LINHA
    try:
        textoDaLinha = texto[LINHA]
    except:
        return
    global LEXICA_CORRETA
    while True:
        while COLUNA < len(textoDaLinha):
            caracter = textoDaLinha[COLUNA]
            # CASO SEJA UM NUMERO  INTEIRO CHAME q1
            if caracter in CARACTER_NUMEROS:
                q1(texto, 0)
                continue
            # CASO EM QUE O CARACTER E UM OPERADOR ALGEBRICO
            if caracter in OPERADORES_ALGEBRICOS:
                q3(texto)
                continue
            # CASO SEJA < , CHAMA QUE Q4 PARA VERIFICAR
            if caracter == '<':
                COLUNA += 1
                q4(texto)
                continue
            # CASO SEJA > , CHAMA QUE Q5 PARA VERIFICAR
            if caracter == '>':
                COLUNA += 1
                q5(texto)
                continue
            # CASO SEJA ALGUM SEPARADOR MATEMATICO CHAMA Q6 (EXEMPLO : "]" )
            if caracter in SEPARADORES_MATEMATICOS:
                q6(texto)
                continue
            # CASO SEJA ALGUM OPERADOR LOGICO CHAMA  Q7 PARA VERIFICAR
            if caracter in OPERADORES_LOGICOS:
                q7(texto)
                continue
            # CASO SEJA UMA LETRA , ENTAO ELE  CHAMA Q8 QUE VAI TRATAR DE TODOS OS IDENTIFICADORES
            if caracter in CARACTER_ALFABETO:
                q8(texto, 0)
                continue
            # CASO SEJA ALGUNS SIBOLOS MAPEADOS NA LINGUAGUEM COMO [";",":","."] CHAMA Q9
            if caracter in SIMBOLOS_LINGUAGEM:
                q9(texto)
                continue
            #  CASO SEJA UMA ASPAS DUPLA , ENTAO CHAMA Q10 QUE VAI TRATAR AS STRINGS
            if caracter == '"':
                COLUNA += 1
                q10(texto, 0)
                try:
                    textoDaLinha = texto[LINHA]
                except:
                    return
                continue
            # CASO A LINHA TERMINE "\n" ANDO NO NUMERO DE LINHA ,ZERO A COLUNA  E TENTO PEGAR O TEXTO DA LINHA , CASO O NUMERO DE LINHA TENHA ESTOURADO O NUMERO DE LINHAS EXISTENTE NO TEXTO ELE FAZ RETURN
            valor = ord(caracter)
            if valor in IGNORE:
                COLUNA += 1
                continue
            # SE ELE NAO ENTROU EM NENHUM CASO E UM CARACTER NAO PERTENCENTE A LIGUAGUEM
            printer(LINHA + 1, COLUNA + 1)
            LEXICA_CORRETA = False
            # ANDANDO NA LINHA
            COLUNA += 1
        LINHA += 1
        try:
            textoDaLinha = texto[LINHA]
            COLUNA = 0
            continue
        except:
            return
# ESTADO Q1 QUE VAI TRATAR OS NUMEROS ( TEM PRINT )
def q1(texto, tamanho):
    global COLUNA
    global LINHA
    global LEXICA_CORRETA
    global TOKENS
    try:
        textoDaLinha = texto[LINHA]
    except:
        return
    token = ""
    while COLUNA < len(textoDaLinha):
        caracter = textoDaLinha[COLUNA]
        # IF QUE MARCA UM ERRO POIS TEMOS UMA LETRA JUNTO COM UM NUMERO
        if caracter in CARACTER_ALFABETO:
            printer(LINHA + 1, COLUNA)
            LEXICA_CORRETA = False
            return
        # IF QUE MARCA O ENCONTRO DE UMA VIRGULA, ENTAO O COMECO DE UM NUMERO REAL, CHAMA Q2 QUE TRATA DE NUMEROS REAIS
        if caracter == ',':
            # ADCIONO A VIRGULA NO TOKEN
            token = token + caracter
            COLUNA += 1
            q2(texto, tamanho + 1, token)
            return
        # NO MEIO DO NUMERO TEM ALGUM SIMBOLO QUE NAO E UMA LETRA, ENTAO MARCA O FINAL DE UM NUMERO
        if caracter not in CARACTER_NUMEROS:
            # CRIANDO O TOKEN E ADCIONANDO
            newToken = Token("numero_inteiro", token)
            TOKENS.append(newToken)
            return
        # ADCIONO O CARACTER QUE AQUI TENHO CERTEZA QUE E UM NUMERO
        token = token + caracter
        # COMO O CARACTER NAO E UM FINALIZADOR ENTAO AUMENTO O TAMANHO DO NUMERO
        tamanho += 1
        # VERIFICADO SE O TAMNHO DO NUMERO NAO PASSOU 512 CARACTER
        if tamanho > MAX_TAMANHO_INTEIRO:
            printer(LINHA + 1, COLUNA)
            LEXICA_CORRETA = False
            return
        # ANDANDO NA LINHA
        COLUNA += 1
    # CASO EM QUE O ULTIMO CARACTER DA LINHA FAZ PARTE DO TOKEN
    newToken = Token("numero_inteiro", token)
    TOKENS.append(newToken)
# ESTADO Q2 QUE VAI TRATAR NUMEROS REAIS ( Q1 CHAMA Q2 ,QUANDO ENCONTRA UMA VIRGULA, O NUEMRO DEIXA DE SER INTEIRO E VIRA REAL) ( TEM PRINT)
def q2(texto, tamanho, token):
    global LEXICA_CORRETA
    global TOKENS
    global COLUNA
    global LINHA
    # VERIFICADO SE O TAMNHO DO NUMERO NAO PASSOU 512 CARACTER, PODE TER ESTOURADO O TAMANHO COM A VIRGULA E Q1 NAO VERIFICA
    if tamanho > MAX_TAMANHO_REAL:
        # ERRO E NA VIRGULA Q1 PASSA PARA Q2 A COLUNA DEPOIS DA VIRGULA
        printer(LINHA + 1, COLUNA - 1)
        LEXICA_CORRETA = False
        COLUNA -= 1
        return
    textoDaLinha = texto[LINHA]
    while COLUNA < len(textoDaLinha):
        caracter = textoDaLinha[COLUNA]
        # IF QUE MARCA O ENCONTRO DE UMA LETRA NO MEIO DE UM NUMERO REAL
        if caracter in CARACTER_ALFABETO or caracter == ",":
            printer(LINHA + 1, COLUNA)
            LEXICA_CORRETA = False
            return
        # NO MEIO  TEM ALGUM SIMBOLO QUE  MARCA O FINAL DO NUMERO REAL
        if caracter not in CARACTER_NUMEROS:
            # CRIANDO O TOKEN E ADCIONANDO
            newToken = Token("numero_real", token)
            TOKENS.append(newToken)
            return
        # SE ELE NAO E UM FINALIZADOR EU ADCIONO ELE NO TOKEN
        token = token + caracter
        # COMO O CARACTER NAO E UM FINALIZADOR ENTAO AUMENTO O TAMANHO DO NUMERO
        tamanho += 1
        if tamanho > MAX_TAMANHO_REAL:
            printer(LINHA + 1, COLUNA)
            LEXICA_CORRETA = False
            return
        # ANDANDO NA LINHA
        COLUNA += 1
    # CASO EM QUE O ULTIMO CARACTER DA LINHA FAZ PARTE DO TOKEN
    newToken = Token("numero_real", token)
    TOKENS.append(newToken)
# ESTADO Q3 QUE VAI TRATAR OPERADORES ALGEBRICOS
def q3(texto):
    global TOKENS
    global COLUNA
    global LINHA
    textoDaLinha = texto[LINHA]
    while COLUNA < len(textoDaLinha):
        caracter = textoDaLinha[COLUNA]
        if caracter == '*':
            # ESTADO QUE VAI TRATAR SE E UM * OU **
            COLUNA += 1
            q11(texto)
            return
        # CASO NAO SEJA NENHUM OPERADOR ALGEBRICO CHAME Q0
        if caracter not in OPERADORES_ALGEBRICOS:
            return
        # CRIANDO O TOKEN E ADCIONANDO
        newToken = Token(caracter, caracter)
        TOKENS.append(newToken)
        # ANDANDO NA LINHA
        COLUNA += 1
# ESTADO Q4 VAI TRATAR O SIMBOLO < E TODAS AS SUAS VARIANTES,ELE JA CHEGA NESSE ESTADO COM PELO MENOS O TOKEN < CRIADO
def q4(texto):
    global COLUNA
    global LINHA
    textoDaLinha = texto[LINHA]
    # Q0 SO CHAMA Q4 DEPOIS DE LER UM < , ENTAO NO INICIO DE QUE Q4 JA TEMOS O TOKEN <
    token = "<"
    global TOKENS
    while COLUNA < len(textoDaLinha):
        caracter = textoDaLinha[COLUNA]
        # CASO O CARACTER SEJA "<" , ENTAO FOI DIGITADO "<<" , GERAMOS O TOKEN "<" E MANDAMOS PARA Q0 NOVAMENTE LER O SEGUNDO <, ASSIM Q0 VAI CHAMAR ESSA FUNCAO DNV
        if caracter == '<':
            # CRIANDO O TOKEN E ADCIONANDO
            newToken = Token(token, token)
            TOKENS.append(newToken)
            return
        # CASO NAO SEJA NENHUM DESSES ENTAO CHAME Q0, POIS ESTA COMECANDO OUTRO TOKEN E ENTAO O TOKEN GERADO FOI SO "<"
        if caracter not in ['=', '>', '-', '<']:
            # CRIANDO O TOKEN E ADCIONANDO
            newToken = Token(token, token)
            TOKENS.append(newToken)
            return
        # CRIANDO TODAS AS POSSIVEIS VARIACOES DE <
        token = token + caracter
        # ENTAO AQUI EU CONCATENO PARA GERAR UMA DAS VARIACOES DE "<" QUE PODEM SER <= , <-, <>
        if token in ["<=", "<>", "<-"]:
            # CRIANDO O TOKEN E ADCIONANDO
            newToken = Token(token, token)
            TOKENS.append(newToken)
            COLUNA += 1
            return
        # ANDANDO NA LINHA
        COLUNA += 1
    # CASO EM QUE O ULTIMO CARACTER DA LINHA FAZ PARTE DO TOKEN
    newToken = Token(token, token)
    TOKENS.append(newToken)
# ESTADO Q5 VAI TRATAR O SIMBOLO > E TODAS AS SUAS VARIANTES
def q5(texto):
    global COLUNA
    global LINHA
    global TOKENS
    textoDaLinha = texto[LINHA]
    # Q0 SO CHAMA Q5 DEPOIS DE LER UM > , ENTAO NO INICIO DE QUE Q5 JA TEMOS O TOKEN >
    token = ">"
    while COLUNA < len(textoDaLinha):
        caracter = textoDaLinha[COLUNA]
        # CASO O CARACTER SEJA ">" , ENTAO FOI DIGITADO ">>" , GERAMOS O TOKEN ">" E MANDAMOS PARA Q0 NOVAMENTE LER O SEGUNDO >, ASSIM Q0 VAI CHAMAR ESSA FUNCAO DNV
        if caracter == ">":
            # CRIANDO O TOKEN E ADCIONANDO
            newToken = Token(token, token)
            TOKENS.append(newToken)
            return
        # CASO NAO SEJA NENHUM DESSES ENTAO CHAME Q0, POIS ESTA COMECANDO OUTRO TOKEN
        if caracter not in ['>', '=']:
            # CRIANDO O TOKEN E ADCIONANDO
            newToken = Token(token, token)
            TOKENS.append(newToken)
            return
        # CRIANDO TODAS AS POSSIVEIS VARIACOES DE >
        token = token + caracter
        if token == ">=":
            # CRIANDO O TOKEN E ADCIONANDO
            newToken = Token(token, token)
            TOKENS.append(newToken)
            COLUNA += 1
            return
        # ANDANDO NA LINHA
        COLUNA += 1
    # CASO EM QUE O ULTIMO CARACTER DA LINHA FAZ PARTE DO TOKEN
    newToken = Token(token, token)
    TOKENS.append(newToken)
# ESTADO Q6 VAI TRATAR OS SEPARADORES MATEMATICOS EX ( "]" OU ")" )
def q6(texto):
    global COLUNA
    global LINHA
    global TOKENS
    textoDaLinha = texto[LINHA]
    while COLUNA < len(textoDaLinha):
        caracter = textoDaLinha[COLUNA]
        # CASO NAO SEJA NENHUM DESSES ENTAO CHAME Q0, POIS ESTA COMECANDO OUTRO TOKEN
        if caracter not in SEPARADORES_MATEMATICOS:
            return
        else:
            # CASO EM QUE O CARACTER E "]" OU ")"
            newToken = Token(caracter, caracter)
            TOKENS.append(newToken)
        # ANDANDO NA LINHA
        COLUNA += 1
# ESTADO Q7 VAI TRATAR OS OPERADORES LOGICOS
def q7(texto):
    global COLUNA
    global LINHA
    textoDaLinha = texto[LINHA]
    global TOKENS
    while COLUNA < len(textoDaLinha):
        caracter = textoDaLinha[COLUNA]
        # CASO NAO SEJA NENHUM DESSES ENTAO CHAME Q0 , POIS ESTA COMECANDO OUTRO TOKEN QUE NAO E TARTADO NESSA FUNCAO
        if caracter not in OPERADORES_LOGICOS:
            return
        else:
            # CASO EM QUE O CARACTER E UM OPERADOR LOGICO
            # CRIANDO O TOKEN E ADCIONANDO
            if caracter == "|":
                newToken = Token("or", caracter)
                TOKENS.append(newToken)
            else:
                newToken = Token(caracter, caracter)
                TOKENS.append(newToken)
        # ANDANDO NA LINHA
        COLUNA += 1
# ESTADO Q8 VAI TRATAR OS IDENTIFICADORES DA LIGUAGUEM ( TEM PRINT )
def q8(texto, tamanho):
    global COLUNA
    global LINHA
    global LEXICA_CORRETA
    global TOKENS
    textoDaLinha = texto[LINHA]
    token = ""
    while COLUNA < len(textoDaLinha):
        caracter = textoDaLinha[COLUNA]
        # NO MEIO DA STRING  TEM ALGUM SIMBOLO SEM SER LETRA NEM NUMERO, MARCANDO O FINAL DO IDENTIFICADOR
        if caracter not in CARACTER_NUMEROS and caracter not in CARACTER_ALFABETO:
            # CRIANDO O TOKEN E ADCIONANDO
            if token in PALAVRAS_RESERVADA:
                tokenCriator(token)
            else:
                newToken = Token("id", token)
                TOKENS.append(newToken)
            return
        # SE ELE NAO E UM FINALIZADOR EU ADCIONO ELE NO TOKEN
        token = token + caracter
        # COMO O CARACTER NAO E UM FINALIZADOR ENTAO AUMENTO O TAMANHO DO NUMERO
        tamanho += 1
        # VERIFICADO SE O TAMANHO DA STRING NAO PASSOU 512 CARACTER
        if tamanho > MAX_TAMANHO_IDNTIFICADOR:
            printer(LINHA + 1, COLUNA)
            LEXICA_CORRETA = False
            return
        # ANDANDO NA LINHA
        COLUNA += 1
    # CASO EM QUE O ULTIMO CARACTER DA LINHA FAZ PARTE DO TOKEN
    if token in PALAVRAS_RESERVADA:
        tokenCriator(token)
    else:
        newToken = Token("id", token)
        TOKENS.append(newToken)
# ESTADO Q9 VAI TRATAR "; ou : ou ."
def q9(texto):
    global COLUNA
    global LINHA
    global TOKENS
    textoDaLinha = texto[LINHA]
    while COLUNA < len(textoDaLinha):
        caracter = textoDaLinha[COLUNA]
        # VERIFICA SE NAO E NENHUM DOS SIMBOLOS RESERVADOS QUE A FUNCAO TRATA, CASO NAO SEJA VAI COMECAR UM OUTRO TOKEN qQUE NAO E TRATADO NESSA FUNCAO
        if caracter not in SIMBOLOS_LINGUAGEM:
            return
        else:
            if caracter == ".":
                newToken = Token("ponto",".")
                TOKENS.append(newToken)
            else:
                newToken = Token(caracter, caracter)
                TOKENS.append(newToken)
        # ANDANDO NA LINHA
        COLUNA += 1
# ESTADO Q10 VAI GERAR AS STRINGS ( TEM PRINT )
def q10(texto, tamanho):
    global TOKENS
    global LEXICA_CORRETA
    global COLUNA
    global LINHA
    textoDaLinha = texto[LINHA]
    token = ""
    caracterAnterior = ""
    linhaAnterior = 0
    # WHILE QUE FAZ A FUNCAO RODAR O PROGRAMA TODAS ATRAS DA SEGUNDA ASPA
    while True:
        while COLUNA < len(textoDaLinha):
            caracter = textoDaLinha[COLUNA]
            # IF QUE MARCA O FINAL DE UMA STRING E INICIO DE OUTRO TOKEN. (ELE FICA PROCURANDO PELA SEGUNDA ASPAS DUPLAS)
            if caracter == '"':
                # CRIANDO O TOKEN E ADCIONANDO
                newToken = Token("string", token)
                TOKENS.append(newToken)
                COLUNA += 1
                return
            # SE ELE NAO E O FINAL DE UMA STRING ENTAO FAZ PARTE DELA , COLOCO O CARACTER NO TOKEN
            token = token + caracter
            # COMO O CARACTER NAO E UM FINALIZADOR ENTAO AUMENTO O TAMANHO DO NUMERO
            tamanho += 1
            # VERIFICADO SE O TAMANHO DA STRING NAO PASSOU 512 CARACTER
            if tamanho > MAX_TAMANHO_STRING:
                if caracterAnterior == '\n':
                    printer(LINHA, len(linhaAnterior))
                    LEXICA_CORRETA = False
                    return
                printer(LINHA + 1, COLUNA)
                LEXICA_CORRETA = False
                return
                # ANDANDO NA LINHA
            COLUNA += 1
            caracterAnterior = caracter

        # MUDANDO DE LINHA
        linhaAnterior = texto[LINHA]
        LINHA += 1
        try:
            textoDaLinha = texto[LINHA]
            COLUNA = 0
            continue
        except:
            # NO ARQUIVO NAO TEM A SEGUNDA ASPA
            printer(LINHA, COLUNA)
            LEXICA_CORRETA = False
            return
# ESTADO Q11 SO E CHAMDO PELO Q3 , ELE VERIFICA SE O OPERADOR ALGEBRICO (*) E UM SO * OU E ** , ENTAO GERA O TOKEN [ESTADO DEPENDENTE DE Q3]
def q11(texto):
    global COLUNA
    global LINHA
    textoDaLinha = texto[LINHA]
    global TOKENS
    while COLUNA < len(textoDaLinha):
        caracter = textoDaLinha[COLUNA]
        # CASO SEJA OUTRO * ENTAO CRIA O TOKEN **, POIS VEIO DOIS SEGUIDOS
        if caracter == '*':
            # CRIANDO O TOKEN E ADCIONANDO
            newToken = Token("**", "**")
            TOKENS.append(newToken)
            COLUNA += 1
            return
        # CASO NAO SEJA *, VAI COMECAR UM NOVO TOKEN
        else:
            # CRIANDO O TOKEN E ADCIONANDO
            newToken = Token("*", "*")
            TOKENS.append(newToken)
            return
        # ANDANDO NA LINHA
        COLUNA += 1
    # CASO NAO TENHA CARACTER NENHUM
    newToken = Token("*", "*")
    TOKENS.append(newToken)
#PRINTER É APENAS O PRINT DE PYTHON2
def printer(linha, coluna):
    print linha , coluna
#VAI CRIAR OS TOKENS ESPECIFICOS PARA AS PALAVARS RESERVADAS DA LINGUAGEM
def tokenCriator(token):
    #OUTROS TOKENS RESERVADOS
    newToken = Token(token.lower(),token)
    TOKENS.append(newToken)
    return
############################################
# ANALIZADOR LEXICO - FIM
############################################
def processadorLinhas(str):
    linhas = []
    linha = ""
    global LEXICA_CORRETA
    for c in str:
        # PEGA O VALOR INTEIRO DO CARACTER
        valor = ord(c)
        # VERIFICA SE ELE E UM CARACTER VALIDO
        if valor == 9 or valor == 10 or (valor > 31 and valor < 127):
            linha = linha + c
        else:
            print "ARQUIVO INVALIDO"
            LEXICA_CORRETA = False
            return linhas
        if c == '\n':
            linhas.append(linha)
            linha = ""
    # PEGANDO A ULTIMA LINHA QUE NAO POSSUI A QUEBRA
    linhas.append(linha)
    # REMOVENDO TODAS AS LINHAS VAZIAS
    val_remove = ""
    while val_remove in linhas:
        try:
            linhas.remove(val_remove)
        except:
            return linhas
    return linhas
############################################
# INICIO MAIN
############################################
def main():
    global LEXICA_CORRETA
    input_str = sys.stdin.read()
    programa = processadorLinhas(input_str)
    if LEXICA_CORRETA:
        q0(programa)
    if LEXICA_CORRETA:
        print "OK"
############################################
# FIM MAIN
############################################
main()