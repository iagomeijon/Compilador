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


class Node:
    def __init__(self, token : Token):
        self.token = token
        self.filhos = []

    def setFilhos(self, filhos):
        self.filhos = filhos

    def setToken(self, token: Token):
        self.token = token

    def getFilhos(self):
        return self.filhos

    def getToken(self):
        return self.token

    def addFilho(self, node):
        self.filhos.append(node)

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
PALAVRAS_RESERVADA = ["ATEH","DE","ENQUANTO","ESCREVA","FIM","FUNCAO","INICIO","INTEIRO","LEIA","NULO","PARA","PARE",
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
    print (linha , coluna)
#VAI CRIAR OS TOKENS ESPECIFICOS PARA AS PALAVARS RESERVADAS DA LINGUAGEM
def tokenCriator(token):
    newToken = Token(token.lower(),token)
    TOKENS.append(newToken)
    return
############################################
# ANALIZADOR LEXICO - FIM
############################################
############################################
# ANALIZADOR SINTATICO - INICIO
############################################
def analisadorSintatico(tokens, tabela):
    #apontador para a entrada corrente
    next = 0
    #inicializando a pilha
    pilha = [0]
    while (True):
        #pegando a entrada
        entrada = tokens[next]
        #olhando o topo da pilha
        topo = pilha.pop()
        pilha.append(topo)
        try:
            #pegando a linha da tabela ( o estado )
            linha = tabela[topo]
            #pegando a acao a ser realizada para a entrada na linha da tabela (estado) [indexando a tabela]
            action = linha[entrada.tipo]
            #caso em que é feito o shift
            if action[0] == "s":
                #empilha a entrada , o proximo estado e move para frente o ponteiro da entrada
                #Cria o novo node (é uma folha), com o token que deveria ser empilhado dentro dele
                newNode = Node(entrada)
                pilha.append(newNode)
                pilha.append(action[1])
                next += 1
            # caso em que é feito a redução
            if action[0] == "r":
                #pega a quantidade de itens quedeve ser retirado da pilha
                vezes = 0
                if action[2] != "ε":
                    vezes = action[2].count(" ") + 1

                # criando o novo node que vai ser empilhado , com o seu token , sem valor associado
                newToken = Token(action[1], "")
                newNode = Node(newToken)
                #retirnado os itens da pilha
                for i in range(vezes * 2):
                    topo = pilha.pop()
                    #Verifico se é um interio ou um node
                    if not isinstance(topo, int):
                        #adiciono esse node como filho do que será empilhado
                        newNode.addFilho(topo)

                #Olhando o topo da pilha, para saber o desvio
                topo = pilha.pop()
                pilha.append(topo)
                #pegando a linha que informa o desvio
                linha = tabela[topo]
                #pegando o desvio
                desvio = linha[action[1]]
                if desvio[0] == "d":
                #empilhando o novo node e o numero do estado que foi desviado
                    pilha.append(newNode)
                    pilha.append(desvio[1])

            #caso em que a entrada é aceita
            if action[0] == "acc":
                return True
        except:
            #caso em que foi indexado alguma coisa que não existe , logo é um erro
            return False

def preencherTable():
    #EXEMPLO DE COMO PREENCHER
    table = []
    q0 = {"var": ["r", "BLOCO_VARIAVEIS", "ε"], "inicio": ["r", "BLOCO_VARIAVEIS", "ε"],"funcao": ["r", "BLOCO_VARIAVEIS", "ε"], "vet": ["s", 7], "inteiro": ["s", 8], "real": ["s", 9],"PROGRAMA": ["d", 1], "BLOCO_VARIAVEIS": ["d", 2], "TIPO": ["d", 6], "VARIAVEL": ["d", 3],"DECLARACAO_ID": ["d", 4], "DECLARACAO_VET": ["d", 5]}
    table.append(q0)
    q1 = {"$": ["acc"]}
    table.append(q1)
    q2 = {"var": ["r", "BLOCO_DEC_FUNC", "ε"], "funcao": ["s", 13], "BLOCO_PROTOTIPO_DEC_FUNC": ["d", 10],"BLOCO_DEC_FUNC": ["d", 12], "DEC_FUNCAO": ["d", 14], "PROT_FUNC": ["d", 11]}
    table.append(q2)
    q3 = {"ponto": ["s", 15]}
    table.append(q3)
    q4 = {"ponto": ["r", "VARIAVEL", "DECLARACAO_ID"]}
    table.append(q4)
    q5 = {"ponto": ["r", "VARIAVEL", "DECLARACAO_VET"]}
    table.append(q5)
    q6 = {":": ["s", 16]}
    table.append(q6)
    q7 = {"inteiro": ["s", 8], "real": ["s", 9], "TIPO": ["d", 17]}
    table.append(q7)
    q8 = {"var": ["r", "TIPO", "inteiro"], "ponto": ["r", "TIPO", "inteiro"], ":": ["r", "TIPO", "inteiro"]}
    table.append(q8)
    q9 = {"var": ["r", "TIPO", "real"], "ponto": ["r", "TIPO", "real"], ":": ["r", "TIPO", "real"]}
    table.append(q9)
    q10 = {"var": ["s", 18]}
    table.append(q10)
    q11 = {"var": ["s", 20], "ponto": ["s", 19]}
    table.append(q11)
    q12 = {"var": ["r", "BLOCO_PROTOTIPO_DEC_FUNC", "BLOCO_DEC_FUNC"]}
    table.append(q12)
    q13 = {"id": ["s", 21]}
    table.append(q13)
    q14 = {"var": ["r", "BLOCO_DEC_FUNC", "ε"], "funcao": ["s", 13], "BLOCO_DEC_FUNC": ["d", 22], "DEC_FUNCAO": ["d", 14],"PROT_FUNC": ["d", 23]}
    table.append(q14)
    q15 = {"var": ["r", "BLOCO_VARIAVEIS", "ε"], "inicio": ["r", "BLOCO_VARIAVEIS", "ε"],"funcao": ["r", "BLOCO_VARIAVEIS", "ε"], "vet": ["s", 7], "inteiro": ["s", 8], "real": ["s", 9],"BLOCO_VARIAVEIS": ["d", 24], "TIPO": ["d", 6], "VARIAVEL": ["d", 3], "DECLARACAO_ID": ["d", 4],"DECLARACAO_VET": ["d", 5]}
    table.append(q15)
    q16 = {"id": ["s", 26], "CONCATENAR_ID": ["d", 25]}
    table.append(q16)
    q17 = {":": ["s", 27]}
    table.append(q17)
    q18 = {"var": ["r", "BLOCO_VARIAVEIS", "ε"], "inicio": ["r", "BLOCO_VARIAVEIS", "ε"],"funcao": ["r", "BLOCO_VARIAVEIS", "ε"], "vet": ["s", 7], "inteiro": ["s", 8], "real": ["s", 9],"BLOCO_VARIAVEIS": ["d", 28], "TIPO": ["d", 6], "VARIAVEL": ["d", 3], "DECLARACAO_ID": ["d", 4],"DECLARACAO_VET": ["d", 5]}
    table.append(q18)
    q19 = {"var": ["r", "BLOCO_DEC_FUNC", "ε"], "funcao": ["s", 13], "BLOCO_PROTOTIPO_DEC_FUNC": ["d", 29],"BLOCO_DEC_FUNC": ["d", 12], "DEC_FUNCAO": ["d", 14], "PROT_FUNC": ["d", 11]}
    table.append(q19)
    q20 = {"var": ["r", "BLOCO_VARIAVEIS", "ε"], "inicio": ["r", "BLOCO_VARIAVEIS", "ε"],"funcao": ["r", "BLOCO_VARIAVEIS", "ε"], "vet": ["s", 7], "inteiro": ["s", 8], "real": ["s", 9],"BLOCO_VARIAVEIS": ["d", 30], "TIPO": ["d", 6], "VARIAVEL": ["d", 3], "DECLARACAO_ID": ["d", 4],"DECLARACAO_VET": ["d", 5]}
    table.append(q20)
    q21 = {"(": ["s", 31]}
    table.append(q21)
    q22 = {"var": ["r", "BLOCO_DEC_FUNC", "DEC_FUNCAO BLOCO_DEC_FUNC"]}
    table.append(q22)
    q23 = {"var": ["s", 20]}
    table.append(q23)
    q24 = {"var": ["r", "BLOCO_VARIAVEIS", "VARIAVEL ponto BLOCO_VARIAVEIS"],"inicio": ["r", "BLOCO_VARIAVEIS", "VARIAVEL ponto BLOCO_VARIAVEIS"],"funcao": ["r", "BLOCO_VARIAVEIS", "VARIAVEL ponto BLOCO_VARIAVEIS"]}
    table.append(q24)
    q25 = {"ponto": ["r", "DECLARACAO_ID", "TIPO : CONCATENAR_ID"]}
    table.append(q25)
    q26 = {"ponto": ["r", "CONCATENAR_ID", "id"], ";": ["s", 32]}
    table.append(q26)
    q27 = {"id": ["s", 33]}
    table.append(q27)
    q28 = {"inicio": ["s", 34]}
    table.append(q28)
    q29 = {"var": ["r", "BLOCO_PROTOTIPO_DEC_FUNC", "PROT_FUNC ponto BLOCO_PROTOTIPO_DEC_FUNC"]}
    table.append(q29)
    q30 = {"inicio": ["s", 35]}
    table.append(q30)
    q31 = {")": ["r", "LISTAR_PARAMETROS", "ε"], "vet": ["s", 39], "inteiro": ["r", "VETOR", "ε"],"real": ["r", "VETOR", "ε"], "LISTAR_PARAMETROS": ["d", 36], "PARAMETROS": ["d", 37], "VETOR": ["d", 38]}
    table.append(q31)
    q32 = {"id": ["s", 26], "CONCATENAR_ID": ["d", 40]}
    table.append(q32)
    q33 = {"numero_inteiro": ["s", 41]}
    table.append(q33)
    q34 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 42], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q34)
    q35 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 59], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q35)
    q36 = {")": ["s", 60]}
    table.append(q36)
    q37 = {")": ["r", "LISTAR_PARAMETROS", "PARAMETROS"]}
    table.append(q37)
    q38 = {"inteiro": ["s", 8], "real": ["s", 9], "TIPO": ["d", 61]}
    table.append(q38)
    q39 = {"inteiro": ["r", "VETOR", "vet"], "real": ["r", "VETOR", "vet"]}
    table.append(q39)
    q40 = {"ponto": ["r", "CONCATENAR_ID", "id ; CONCATENAR_ID"]}
    table.append(q40)
    q41 = {"ponto": ["r", "DECLARACAO_VET", "vet TIPO : id numero_inteiro"]}
    table.append(q41)
    q42 = {"fim": ["s", 62]}
    table.append(q42)
    q43 = {"ponto": ["s", 63]}
    table.append(q43)
    q44 = {"ponto": ["s", 64]}
    table.append(q44)
    q45 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 65], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q45)
    q46 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 66], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q46)
    q47 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 67], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43], "ATRIBUICAO": ["d", 44]}
    table.append(q47)
    q48 = {"ponto": ["s", 68]}
    table.append(q48)
    q49 = {"ponto": ["s", 69]}
    table.append(q49)
    q50 = {"ponto": ["s", 70]}
    table.append(q50)
    q51 = {"ponto": ["s", 71]}
    table.append(q51)
    q52 = {"(": ["s", 72], "[": ["s", 74], "<-": ["r", "INDEX", "ε"], "INDEX": ["d", 73]}
    table.append(q52)
    q53 = {"id": ["r", "SINAL", "ε"], "(": ["s", 81], "!": ["s", 78], "-": ["s", 87],"numero_inteiro": ["r", "SINAL", "ε"], "numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 82],"EXP_RELACIONAL_TOTAL": ["d", 75], "EXP_RELACIONAL_N2": ["d", 76], "EXP_RELACIONAL_N3": ["d", 77],"EXP_RELACIONAL_FINAL": ["d", 79], "EXP_RELACIONAL_SIMPLES": ["d", 80], "EXP_N2": ["d", 83],"EXP_N3": ["d", 84], "EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q53)
    q54 = {"id": ["r", "SINAL", "ε"], "(": ["s", 81], "!": ["s", 78], "-": ["s", 87],"numero_inteiro": ["r", "SINAL", "ε"], "numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 82],"EXP_RELACIONAL_TOTAL": ["d", 88], "EXP_RELACIONAL_N2": ["d", 76], "EXP_RELACIONAL_N3": ["d", 77],"EXP_RELACIONAL_FINAL": ["d", 79], "EXP_RELACIONAL_SIMPLES": ["d", 80], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84], "EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q54)
    q55 = {"id": ["s", 89]}
    table.append(q55)
    q56 = {"id": ["s", 91], "CONCATENAR_LEIA": ["d", 90]}
    table.append(q56)
    q57 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "string": ["s", 93], "-": ["s", 87],"numero_inteiro": ["r", "SINAL", "ε"], "numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 94],"LISTA_ESCREVA": ["d", 92], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84], "EXP_FINAL": ["d", 85],"SINAL": ["d", 86]}
    table.append(q57)
    q58 = {"ponto": ["r", "RECEBA", "receba"], "(": ["s", 96]}
    table.append(q58)
    q59 = {"fim": ["s", 97]}
    table.append(q59)
    q60 = {":": ["s", 98]}
    table.append(q60)
    q61 = {":": ["s", 99]}
    table.append(q61)
    q62 = {"$": ["r", "PROGRAMA", "BLOCO_VARIAVEIS BLOCO_PROTOTIPO_DEC_FUNC var BLOCO_VARIAVEIS inicio BLOCO_COMANDO fim"]}
    table.append(q62)
    q63 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 100], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q63)
    q64 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 101], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q64)
    q65 = {"fim": ["r", "BLOCO_COMANDO", "BLOCO_IF BLOCO_COMANDO"]}
    table.append(q65)
    q66 = {"fim": ["r", "BLOCO_COMANDO", "BLOCO_ENQUANTO BLOCO_COMANDO"]}
    table.append(q66)
    q67 = {"fim": ["r", "BLOCO_COMANDO", "BLOCO_ATEH BLOCO_COMANDO"]}
    table.append(q67)
    q68 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 102], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q68)
    q69 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 103], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q69)
    q70 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 104], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q70)
    q71 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 105], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q71)
    q72 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], ")": ["r", "LISTAR_PARAMETROS_CHAMADA", "ε"], "-": ["s", 87],"numero_inteiro": ["r", "SINAL", "ε"], "numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 108],"EXP_N2": ["d", 83], "EXP_N3": ["d", 84], "EXP_FINAL": ["d", 85], "SINAL": ["d", 86],"LISTAR_PARAMETROS_CHAMADA": ["d", 106], "CONCATENAR_EXP": ["d", 107]}
    table.append(q72)
    q73 = {"<-": ["s", 109]}
    table.append(q73)
    q74 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 110], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84],"EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q74)
    q75 = {"inicio": ["s", 111]}
    table.append(q75)
    q76 = {"inicio": ["r", "EXP_RELACIONAL_TOTAL", "EXP_RELACIONAL_N2"],")": ["r", "EXP_RELACIONAL_TOTAL", "EXP_RELACIONAL_N2"], "or": ["s", 112]}
    table.append(q76)
    q77 = {"inicio": ["r", "EXP_RELACIONAL_N2", "EXP_RELACIONAL_N3"], ")": ["r", "EXP_RELACIONAL_N2", "EXP_RELACIONAL_N3"],"or": ["r", "EXP_RELACIONAL_N2", "EXP_RELACIONAL_N3"], "&": ["s", 113]}
    table.append(q77)
    q78 = {"id": ["r", "SINAL", "ε"], "(": ["s", 81], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 82], "EXP_RELACIONAL_FINAL": ["d", 114],"EXP_RELACIONAL_SIMPLES": ["d", 80], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84], "EXP_FINAL": ["d", 85],"SINAL": ["d", 86]}
    table.append(q78)
    q79 = {"inicio": ["r", "EXP_RELACIONAL_N3", "EXP_RELACIONAL_FINAL"],")": ["r", "EXP_RELACIONAL_N3", "EXP_RELACIONAL_FINAL"],"or": ["r", "EXP_RELACIONAL_N3", "EXP_RELACIONAL_FINAL"],"&": ["r", "EXP_RELACIONAL_N3", "EXP_RELACIONAL_FINAL"]}
    table.append(q79)
    q80 = {"inicio": ["r", "EXP_RELACIONAL_FINAL", "EXP_RELACIONAL_SIMPLES"],")": ["r", "EXP_RELACIONAL_FINAL", "EXP_RELACIONAL_SIMPLES"],"or": ["r", "EXP_RELACIONAL_FINAL", "EXP_RELACIONAL_SIMPLES"],"&": ["r", "EXP_RELACIONAL_FINAL", "EXP_RELACIONAL_SIMPLES"]}
    table.append(q80)
    q81 = {"id": ["r", "SINAL", "ε"], "(": ["s", 81], "!": ["s", 78], "-": ["s", 87],"numero_inteiro": ["r", "SINAL", "ε"], "numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 116],"EXP_RELACIONAL_TOTAL": ["d", 115], "EXP_RELACIONAL_N2": ["d", 76], "EXP_RELACIONAL_N3": ["d", 77],"EXP_RELACIONAL_FINAL": ["d", 79], "EXP_RELACIONAL_SIMPLES": ["d", 80], "EXP_N2": ["d", 83],"EXP_N3": ["d", 84], "EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q81)
    q82 = {"=": ["s", 118], "<": ["s", 119], "<=": ["s", 120], ">": ["s", 121], ">=": ["s", 122], "<>": ["s", 123],"RELACIONAIS": ["d", 117]}
    table.append(q82)
    q83 = {"inicio": ["r", "EXP", "EXP_N2"], "ponto": ["r", "EXP", "EXP_N2"], ")": ["r", "EXP", "EXP_N2"],";": ["r", "EXP", "EXP_N2"], "]": ["r", "EXP", "EXP_N2"], "ateh": ["r", "EXP", "EXP_N2"],"or": ["r", "EXP", "EXP_N2"], "&": ["r", "EXP", "EXP_N2"], "=": ["r", "EXP", "EXP_N2"],"<": ["r", "EXP", "EXP_N2"], "<=": ["r", "EXP", "EXP_N2"], ">": ["r", "EXP", "EXP_N2"],">=": ["r", "EXP", "EXP_N2"], "<>": ["r", "EXP", "EXP_N2"], "+": ["s", 125], "-": ["s", 126],"SOMA_SUB": ["d", 124]}
    table.append(q83)
    q84 = {"inicio": ["r", "EXP_N2", "EXP_N3"], "ponto": ["r", "EXP_N2", "EXP_N3"], ")": ["r", "EXP_N2", "EXP_N3"],";": ["r", "EXP_N2", "EXP_N3"], "]": ["r", "EXP_N2", "EXP_N3"], "ateh": ["r", "EXP_N2", "EXP_N3"],"or": ["r", "EXP_N2", "EXP_N3"], "&": ["r", "EXP_N2", "EXP_N3"], "=": ["r", "EXP_N2", "EXP_N3"],"<": ["r", "EXP_N2", "EXP_N3"], "<=": ["r", "EXP_N2", "EXP_N3"], ">": ["r", "EXP_N2", "EXP_N3"],">=": ["r", "EXP_N2", "EXP_N3"], "<>": ["r", "EXP_N2", "EXP_N3"], "+": ["r", "EXP_N2", "EXP_N3"],"-": ["r", "EXP_N2", "EXP_N3"], "*": ["s", 128], "/": ["s", 129], "%": ["s", 130], "MULTI_DIV_REST": ["d", 127]}
    table.append(q84)
    q85 = {"inicio": ["r", "EXP_N3", "EXP_FINAL"], "ponto": ["r", "EXP_N3", "EXP_FINAL"],")": ["r", "EXP_N3", "EXP_FINAL"], ";": ["r", "EXP_N3", "EXP_FINAL"], "]": ["r", "EXP_N3", "EXP_FINAL"],"ateh": ["r", "EXP_N3", "EXP_FINAL"], "or": ["r", "EXP_N3", "EXP_FINAL"], "&": ["r", "EXP_N3", "EXP_FINAL"],"=": ["r", "EXP_N3", "EXP_FINAL"], "<": ["r", "EXP_N3", "EXP_FINAL"], "<=": ["r", "EXP_N3", "EXP_FINAL"],">": ["r", "EXP_N3", "EXP_FINAL"], ">=": ["r", "EXP_N3", "EXP_FINAL"], "<>": ["r", "EXP_N3", "EXP_FINAL"],"**": ["s", 131], "+": ["r", "EXP_N3", "EXP_FINAL"], "-": ["r", "EXP_N3", "EXP_FINAL"],"*": ["r", "EXP_N3", "EXP_FINAL"], "/": ["r", "EXP_N3", "EXP_FINAL"], "%": ["r", "EXP_N3", "EXP_FINAL"]}
    table.append(q85)
    q86 = {"id": ["s", 132], "numero_inteiro": ["s", 135], "numero_real": ["s", 136], "CHAMADA_FUNC": ["d", 134],"NUM": ["d", 133]}
    table.append(q86)
    q87 = {"id": ["r", "SINAL", "-"], "(": ["s", 137], "numero_inteiro": ["r", "SINAL", "-"],"numero_real": ["r", "SINAL", "-"]}
    table.append(q87)
    q88 = {"inicio": ["s", 138]}
    table.append(q88)
    q89 = {"de": ["s", 139]}
    table.append(q89)
    q90 = {"ponto": ["r", "LEIA", "leia CONCATENAR_LEIA"]}
    table.append(q90)
    q91 = {"ponto": ["r", "CONCATENAR_LEIA", "id"], ";": ["s", 140], "[": ["s", 141]}
    table.append(q91)
    q92 = {"ponto": ["r", "ESCREVA", "escreva LISTA_ESCREVA"]}
    table.append(q92)
    q93 = {"ponto": ["r", "LISTA_ESCREVA", "string"], ";": ["s", 142]}
    table.append(q93)
    q94 = {"ponto": ["r", "LISTA_ESCREVA", "EXP"], ";": ["s", 143]}
    table.append(q94)
    q95 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 144], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84],"EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q95)
    q96 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 145], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84],"EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q96)
    q97 = {"var": ["r", "DEC_FUNCAO", "PROT_FUNC var BLOCO_VARIAVEIS inicio BLOCO_COMANDO fim"],"funcao": ["r", "DEC_FUNCAO", "PROT_FUNC var BLOCO_VARIAVEIS inicio BLOCO_COMANDO fim"]}
    table.append(q97)
    q98 = {"nulo": ["s", 148], "inteiro": ["s", 8], "real": ["s", 9], "TIPO_RETORNO": ["d", 146], "TIPO": ["d", 147]}
    table.append(q98)
    q99 = {"id": ["s", 149]}
    table.append(q99)
    q100 = {"fim": ["r", "BLOCO_COMANDO", "CHAMADA_FUNC ponto BLOCO_COMANDO"]}
    table.append(q100)
    q101 = {"fim": ["r", "BLOCO_COMANDO", "ATRIBUICAO ponto BLOCO_COMANDO"]}
    table.append(q101)
    q102 = {"fim": ["r", "BLOCO_COMANDO", "LEIA ponto BLOCO_COMANDO"]}
    table.append(q102)
    q103 = {"fim": ["r", "BLOCO_COMANDO", "ESCREVA ponto BLOCO_COMANDO"]}
    table.append(q103)
    q104 = {"fim": ["r", "BLOCO_COMANDO", "pare ponto BLOCO_COMANDO"]}
    table.append(q104)
    q105 = {"fim": ["r", "BLOCO_COMANDO", "RECEBA ponto BLOCO_COMANDO"]}
    table.append(q105)
    q106 = {")": ["s", 150]}
    table.append(q106)
    q107 = {")": ["r", "LISTAR_PARAMETROS_CHAMADA", "CONCATENAR_EXP"]}
    table.append(q107)
    q108 = {")": ["r", "CONCATENAR_EXP", "EXP"], ";": ["s", 151]}
    table.append(q108)
    q109 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 152], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84],"EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q109)
    q110 = {"]": ["s", 153]}
    table.append(q110)
    q111 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 154], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q111)
    q112 = {"id": ["r", "SINAL", "ε"], "(": ["s", 81], "!": ["s", 78], "-": ["s", 87],"numero_inteiro": ["r", "SINAL", "ε"], "numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 82],"EXP_RELACIONAL_TOTAL": ["d", 155], "EXP_RELACIONAL_N2": ["d", 76], "EXP_RELACIONAL_N3": ["d", 77],"EXP_RELACIONAL_FINAL": ["d", 79], "EXP_RELACIONAL_SIMPLES": ["d", 80], "EXP_N2": ["d", 83],"EXP_N3": ["d", 84], "EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q112)
    q113 = {"id": ["r", "SINAL", "ε"], "(": ["s", 81], "!": ["s", 78], "-": ["s", 87],"numero_inteiro": ["r", "SINAL", "ε"], "numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 82],"EXP_RELACIONAL_N2": ["d", 156], "EXP_RELACIONAL_N3": ["d", 77], "EXP_RELACIONAL_FINAL": ["d", 79],"EXP_RELACIONAL_SIMPLES": ["d", 80], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84], "EXP_FINAL": ["d", 85],"SINAL": ["d", 86]}
    table.append(q113)
    q114 = {"inicio": ["r", "EXP_RELACIONAL_N3", "! EXP_RELACIONAL_FINAL"],")": ["r", "EXP_RELACIONAL_N3", "! EXP_RELACIONAL_FINAL"],"or": ["r", "EXP_RELACIONAL_N3", "! EXP_RELACIONAL_FINAL"],"&": ["r", "EXP_RELACIONAL_N3", "! EXP_RELACIONAL_FINAL"]}
    table.append(q114)
    q115 = {")": ["s", 157]}
    table.append(q115)
    q116 = {")": ["s", 158], "=": ["s", 118], "<": ["s", 119], "<=": ["s", 120], ">": ["s", 121], ">=": ["s", 122],"<>": ["s", 123], "RELACIONAIS": ["d", 117]}
    table.append(q116)
    q117 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 159], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84],"EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q117)
    q118 = {"id": ["r", "RELACIONAIS", "="], "(": ["r", "RELACIONAIS", "="], "-": ["r", "RELACIONAIS", "="],"numero_inteiro": ["r", "RELACIONAIS", "="], "numero_real": ["r", "RELACIONAIS", "="]}
    table.append(q118)
    q119 = {"id": ["r", "RELACIONAIS", "<"], "(": ["r", "RELACIONAIS", "<"], "-": ["r", "RELACIONAIS", "<"],"numero_inteiro": ["r", "RELACIONAIS", "<"], "numero_real": ["r", "RELACIONAIS", "<"]}
    table.append(q119)
    q120 = {"id": ["r", "RELACIONAIS", "<="], "(": ["r", "RELACIONAIS", "<="], "-": ["r", "RELACIONAIS", "<="],"numero_inteiro": ["r", "RELACIONAIS", "<="], "numero_real": ["r", "RELACIONAIS", "<="]}
    table.append(q120)
    q121 = {"id": ["r", "RELACIONAIS", ">"], "(": ["r", "RELACIONAIS", ">"], "-": ["r", "RELACIONAIS", ">"],"numero_inteiro": ["r", "RELACIONAIS", ">"], "numero_real": ["r", "RELACIONAIS", ">"]}
    table.append(q121)
    q122 = {"id": ["r", "RELACIONAIS", ">="], "(": ["r", "RELACIONAIS", ">="], "-": ["r", "RELACIONAIS", ">="],"numero_inteiro": ["r", "RELACIONAIS", ">="], "numero_real": ["r", "RELACIONAIS", ">="]}
    table.append(q122)
    q123 = {"id": ["r", "RELACIONAIS", "<>"], "(": ["r", "RELACIONAIS", "<>"], "-": ["r", "RELACIONAIS", "<>"],"numero_inteiro": ["r", "RELACIONAIS", "<>"], "numero_real": ["r", "RELACIONAIS", "<>"]}
    table.append(q123)
    q124 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 160], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84],"EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q124)
    q125 = {"id": ["r", "SOMA_SUB", "+"], "(": ["r", "SOMA_SUB", "+"], "-": ["r", "SOMA_SUB", "+"],"numero_inteiro": ["r", "SOMA_SUB", "+"], "numero_real": ["r", "SOMA_SUB", "+"]}
    table.append(q125)
    q126 = {"id": ["r", "SOMA_SUB", "-"], "(": ["r", "SOMA_SUB", "-"], "-": ["r", "SOMA_SUB", "-"],"numero_inteiro": ["r", "SOMA_SUB", "-"], "numero_real": ["r", "SOMA_SUB", "-"]}
    table.append(q126)
    q127 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP_N2": ["d", 161], "EXP_N3": ["d", 84], "EXP_FINAL": ["d", 85],"SINAL": ["d", 86]}
    table.append(q127)
    q128 = {"id": ["r", "MULTI_DIV_REST", "*"], "(": ["r", "MULTI_DIV_REST", "*"], "-": ["r", "MULTI_DIV_REST", "*"],"numero_inteiro": ["r", "MULTI_DIV_REST", "*"], "numero_real": ["r", "MULTI_DIV_REST", "*"]}
    table.append(q128)
    q129 = {"id": ["r", "MULTI_DIV_REST", "/"], "(": ["r", "MULTI_DIV_REST", "/"], "-": ["r", "MULTI_DIV_REST", "/"],"numero_inteiro": ["r", "MULTI_DIV_REST", "/"], "numero_real": ["r", "MULTI_DIV_REST", "/"]}
    table.append(q129)
    q130 = {"id": ["r", "MULTI_DIV_REST", "%"], "(": ["r", "MULTI_DIV_REST", "%"], "-": ["r", "MULTI_DIV_REST", "%"],"numero_inteiro": ["r", "MULTI_DIV_REST", "%"], "numero_real": ["r", "MULTI_DIV_REST", "%"]}
    table.append(q130)
    q131 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP_N3": ["d", 162], "EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q131)
    q132 = {"inicio": ["r", "EXP_FINAL", "SINAL id"], "ponto": ["r", "EXP_FINAL", "SINAL id"], "(": ["s", 72],")": ["r", "EXP_FINAL", "SINAL id"], ";": ["r", "EXP_FINAL", "SINAL id"], "[": ["s", 163],"]": ["r", "EXP_FINAL", "SINAL id"], "ateh": ["r", "EXP_FINAL", "SINAL id"],"or": ["r", "EXP_FINAL", "SINAL id"], "&": ["r", "EXP_FINAL", "SINAL id"], "=": ["r", "EXP_FINAL", "SINAL id"],"<": ["r", "EXP_FINAL", "SINAL id"], "<=": ["r", "EXP_FINAL", "SINAL id"], ">": ["r", "EXP_FINAL", "SINAL id"],">=": ["r", "EXP_FINAL", "SINAL id"], "<>": ["r", "EXP_FINAL", "SINAL id"],"**": ["r", "EXP_FINAL", "SINAL id"], "+": ["r", "EXP_FINAL", "SINAL id"], "-": ["r", "EXP_FINAL", "SINAL id"],"*": ["r", "EXP_FINAL", "SINAL id"], "/": ["r", "EXP_FINAL", "SINAL id"], "%": ["r", "EXP_FINAL", "SINAL id"]}
    table.append(q132)
    q133 = {"inicio": ["r", "EXP_FINAL", "SINAL NUM"], "ponto": ["r", "EXP_FINAL", "SINAL NUM"],")": ["r", "EXP_FINAL", "SINAL NUM"], ";": ["r", "EXP_FINAL", "SINAL NUM"],"]": ["r", "EXP_FINAL", "SINAL NUM"], "ateh": ["r", "EXP_FINAL", "SINAL NUM"],"or": ["r", "EXP_FINAL", "SINAL NUM"], "&": ["r", "EXP_FINAL", "SINAL NUM"],"=": ["r", "EXP_FINAL", "SINAL NUM"], "<": ["r", "EXP_FINAL", "SINAL NUM"],"<=": ["r", "EXP_FINAL", "SINAL NUM"], ">": ["r", "EXP_FINAL", "SINAL NUM"],">=": ["r", "EXP_FINAL", "SINAL NUM"], "<>": ["r", "EXP_FINAL", "SINAL NUM"],"**": ["r", "EXP_FINAL", "SINAL NUM"], "+": ["r", "EXP_FINAL", "SINAL NUM"],"-": ["r", "EXP_FINAL", "SINAL NUM"], "*": ["r", "EXP_FINAL", "SINAL NUM"],"/": ["r", "EXP_FINAL", "SINAL NUM"], "%": ["r", "EXP_FINAL", "SINAL NUM"]}
    table.append(q133)
    q134 = {"inicio": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"], "ponto": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"],")": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"], ";": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"],"]": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"], "ateh": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"],"or": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"], "&": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"],"=": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"], "<": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"],"<=": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"], ">": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"],">=": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"], "<>": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"],"**": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"], "+": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"],"-": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"], "*": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"],"/": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"], "%": ["r", "EXP_FINAL", "SINAL CHAMADA_FUNC"]}
    table.append(q134)
    q135 = {"inicio": ["r", "NUM", "numero_inteiro"], "ponto": ["r", "NUM", "numero_inteiro"],")": ["r", "NUM", "numero_inteiro"], ";": ["r", "NUM", "numero_inteiro"], "]": ["r", "NUM", "numero_inteiro"],"ateh": ["r", "NUM", "numero_inteiro"], "or": ["r", "NUM", "numero_inteiro"],"&": ["r", "NUM", "numero_inteiro"], "=": ["r", "NUM", "numero_inteiro"], "<": ["r", "NUM", "numero_inteiro"],"<=": ["r", "NUM", "numero_inteiro"], ">": ["r", "NUM", "numero_inteiro"], ">=": ["r", "NUM", "numero_inteiro"],"<>": ["r", "NUM", "numero_inteiro"], "**": ["r", "NUM", "numero_inteiro"], "+": ["r", "NUM", "numero_inteiro"],"-": ["r", "NUM", "numero_inteiro"], "*": ["r", "NUM", "numero_inteiro"], "/": ["r", "NUM", "numero_inteiro"],"%": ["r", "NUM", "numero_inteiro"]}
    table.append(q135)
    q136 = {"inicio": ["r", "NUM", "numero_real"], "ponto": ["r", "NUM", "numero_real"], ")": ["r", "NUM", "numero_real"],";": ["r", "NUM", "numero_real"], "]": ["r", "NUM", "numero_real"], "ateh": ["r", "NUM", "numero_real"],"or": ["r", "NUM", "numero_real"], "&": ["r", "NUM", "numero_real"], "=": ["r", "NUM", "numero_real"],"<": ["r", "NUM", "numero_real"], "<=": ["r", "NUM", "numero_real"], ">": ["r", "NUM", "numero_real"],">=": ["r", "NUM", "numero_real"], "<>": ["r", "NUM", "numero_real"], "**": ["r", "NUM", "numero_real"],"+": ["r", "NUM", "numero_real"], "-": ["r", "NUM", "numero_real"], "*": ["r", "NUM", "numero_real"],"/": ["r", "NUM", "numero_real"], "%": ["r", "NUM", "numero_real"]}
    table.append(q136)
    q137 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 164], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84],"EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q137)
    q138 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 165], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q138)
    q139 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 166], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84],"EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q139)
    q140 = {"id": ["s", 91], "CONCATENAR_LEIA": ["d", 167]}
    table.append(q140)
    q141 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 168], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84],"EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q141)
    q142 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "string": ["s", 93], "-": ["s", 87],"numero_inteiro": ["r", "SINAL", "ε"], "numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 94],"LISTA_ESCREVA": ["d", 169], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84], "EXP_FINAL": ["d", 85],"SINAL": ["d", 86]}
    table.append(q142)
    q143 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "string": ["s", 93], "-": ["s", 87],"numero_inteiro": ["r", "SINAL", "ε"], "numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 94],"LISTA_ESCREVA": ["d", 170], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84], "EXP_FINAL": ["d", 85],"SINAL": ["d", 86]}
    table.append(q143)
    q144 = {")": ["s", 158]}
    table.append(q144)
    q145 = {")": ["s", 171]}
    table.append(q145)
    q146 = {"var": ["r", "PROT_FUNC", "funcao id ( LISTAR_PARAMETROS ) : TIPO_RETORNO"],"ponto": ["r", "PROT_FUNC", "funcao id ( LISTAR_PARAMETROS ) : TIPO_RETORNO"]}
    table.append(q146)
    q147 = {"var": ["r", "TIPO_RETORNO", "TIPO"], "ponto": ["r", "TIPO_RETORNO", "TIPO"]}
    table.append(q147)
    q148 = {"var": ["r", "TIPO_RETORNO", "nulo"], "ponto": ["r", "TIPO_RETORNO", "nulo"]}
    table.append(q148)
    q149 = {")": ["r", "PARAMETROS", "VETOR TIPO : id"], ";": ["s", 172]}
    table.append(q149)
    q150 = {"inicio": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"ponto": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],")": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],";": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"]": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"ateh": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"or": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"&": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"=": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"<": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"<=": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],">": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],">=": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"<>": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"**": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"+": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"-": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"*": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"/": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"],"%": ["r", "CHAMADA_FUNC", "id ( LISTAR_PARAMETROS_CHAMADA )"]}
    table.append(q150)
    q151 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 108], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84],"EXP_FINAL": ["d", 85], "SINAL": ["d", 86], "CONCATENAR_EXP": ["d", 173]}
    table.append(q151)
    q152 = {"ponto": ["r", "ATRIBUICAO", "id INDEX <- EXP"]}
    table.append(q152)
    q153 = {"<-": ["r", "INDEX", "[ EXP ]"]}
    table.append(q153)
    q154 = {"fim": ["s", 174]}
    table.append(q154)
    q155 = {"inicio": ["r", "EXP_RELACIONAL_TOTAL", "EXP_RELACIONAL_N2 or EXP_RELACIONAL_TOTAL"],")": ["r", "EXP_RELACIONAL_TOTAL", "EXP_RELACIONAL_N2 or EXP_RELACIONAL_TOTAL"]}
    table.append(q155)
    q156 = {"inicio": ["r", "EXP_RELACIONAL_N2", "EXP_RELACIONAL_N3 & EXP_RELACIONAL_N2"],")": ["r", "EXP_RELACIONAL_N2", "EXP_RELACIONAL_N3 & EXP_RELACIONAL_N2"],"or": ["r", "EXP_RELACIONAL_N2", "EXP_RELACIONAL_N3 & EXP_RELACIONAL_N2"]}
    table.append(q156)
    q157 = {"inicio": ["r", "EXP_RELACIONAL_FINAL", "( EXP_RELACIONAL_TOTAL )"],")": ["r", "EXP_RELACIONAL_FINAL", "( EXP_RELACIONAL_TOTAL )"],"or": ["r", "EXP_RELACIONAL_FINAL", "( EXP_RELACIONAL_TOTAL )"],"&": ["r", "EXP_RELACIONAL_FINAL", "( EXP_RELACIONAL_TOTAL )"]}
    table.append(q157)
    q158 = {"inicio": ["r", "EXP_FINAL", "( EXP )"], "ponto": ["r", "EXP_FINAL", "( EXP )"],")": ["r", "EXP_FINAL", "( EXP )"], ";": ["r", "EXP_FINAL", "( EXP )"], "]": ["r", "EXP_FINAL", "( EXP )"],"ateh": ["r", "EXP_FINAL", "( EXP )"], "or": ["r", "EXP_FINAL", "( EXP )"], "&": ["r", "EXP_FINAL", "( EXP )"],"=": ["r", "EXP_FINAL", "( EXP )"], "<": ["r", "EXP_FINAL", "( EXP )"], "<=": ["r", "EXP_FINAL", "( EXP )"],">": ["r", "EXP_FINAL", "( EXP )"], ">=": ["r", "EXP_FINAL", "( EXP )"], "<>": ["r", "EXP_FINAL", "( EXP )"],"**": ["r", "EXP_FINAL", "( EXP )"], "+": ["r", "EXP_FINAL", "( EXP )"], "-": ["r", "EXP_FINAL", "( EXP )"],"*": ["r", "EXP_FINAL", "( EXP )"], "/": ["r", "EXP_FINAL", "( EXP )"], "%": ["r", "EXP_FINAL", "( EXP )"]}
    table.append(q158)
    q159 = {"inicio": ["r", "EXP_RELACIONAL_SIMPLES", "EXP RELACIONAIS EXP"],")": ["r", "EXP_RELACIONAL_SIMPLES", "EXP RELACIONAIS EXP"],"or": ["r", "EXP_RELACIONAL_SIMPLES", "EXP RELACIONAIS EXP"],"&": ["r", "EXP_RELACIONAL_SIMPLES", "EXP RELACIONAIS EXP"]}
    table.append(q159)
    q160 = {"inicio": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"], "ponto": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"],")": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"], ";": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"],"]": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"], "ateh": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"],"or": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"], "&": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"],"=": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"], "<": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"],"<=": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"], ">": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"],">=": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"], "<>": ["r", "EXP", "EXP_N2 SOMA_SUB EXP"]}
    table.append(q160)
    q161 = {"inicio": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"],"ponto": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"], ")": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"],";": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"], "]": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"],"ateh": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"], "or": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"],"&": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"], "=": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"],"<": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"], "<=": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"], ">": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"], ">=": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"],"<>": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"], "+": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"],"-": ["r", "EXP_N2", "EXP_N3 MULTI_DIV_REST EXP_N2"]}
    table.append(q161)
    q162 = {"inicio": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"], "ponto": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"],")": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"], ";": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"],"]": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"], "ateh": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"],"or": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"], "&": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"],"=": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"], "<": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"],"<=": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"], ">": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"],">=": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"], "<>": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"],"+": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"], "-": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"],"*": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"], "/": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"],"%": ["r", "EXP_N3", "EXP_FINAL ** EXP_N3"]}
    table.append(q162)
    q163 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 175], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84],"EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q163)
    q164 = {")": ["s", 176]}
    table.append(q164)
    q165 = {"fim": ["s", 177]}
    table.append(q165)
    q166 = {"ateh": ["s", 178]}
    table.append(q166)
    q167 = {"ponto": ["r", "CONCATENAR_LEIA", "id ; CONCATENAR_LEIA"]}
    table.append(q167)
    q168 = {"]": ["s", 179]}
    table.append(q168)
    q169 = {"ponto": ["r", "LISTA_ESCREVA", "string ; LISTA_ESCREVA"]}
    table.append(q169)
    q170 = {"ponto": ["r", "LISTA_ESCREVA", "EXP ; LISTA_ESCREVA"]}
    table.append(q170)
    q171 = {"ponto": ["r", "RECEBA", "receba ( EXP )"]}
    table.append(q171)
    q172 = {"vet": ["s", 39], "inteiro": ["r", "VETOR", "ε"], "real": ["r", "VETOR", "ε"], "PARAMETROS": ["d", 180],"VETOR": ["d", 38]}
    table.append(q172)
    q173 = {")": ["r", "CONCATENAR_EXP", "EXP ; CONCATENAR_EXP"]}
    table.append(q173)
    q174 = {"fim": ["r", "BLOCO_SENAO", "ε"], "id": ["r", "BLOCO_SENAO", "ε"], "receba": ["r", "BLOCO_SENAO", "ε"],"escreva": ["r", "BLOCO_SENAO", "ε"], "leia": ["r", "BLOCO_SENAO", "ε"], "para": ["r", "BLOCO_SENAO", "ε"],"enquanto": ["r", "BLOCO_SENAO", "ε"], "se": ["r", "BLOCO_SENAO", "ε"], "senao": ["s", 182],"pare": ["r", "BLOCO_SENAO", "ε"], "BLOCO_SENAO": ["d", 181]}
    table.append(q174)
    q175 = {"]": ["s", 183]}
    table.append(q175)
    q176 = {"inicio": ["r", "EXP_FINAL", "- ( EXP )"], "ponto": ["r", "EXP_FINAL", "- ( EXP )"],")": ["r", "EXP_FINAL", "- ( EXP )"], ";": ["r", "EXP_FINAL", "- ( EXP )"],"]": ["r", "EXP_FINAL", "- ( EXP )"], "ateh": ["r", "EXP_FINAL", "- ( EXP )"],"or": ["r", "EXP_FINAL", "- ( EXP )"], "&": ["r", "EXP_FINAL", "- ( EXP )"],"=": ["r", "EXP_FINAL", "- ( EXP )"], "<": ["r", "EXP_FINAL", "- ( EXP )"],"<=": ["r", "EXP_FINAL", "- ( EXP )"], ">": ["r", "EXP_FINAL", "- ( EXP )"],">=": ["r", "EXP_FINAL", "- ( EXP )"], "<>": ["r", "EXP_FINAL", "- ( EXP )"],"**": ["r", "EXP_FINAL", "- ( EXP )"], "+": ["r", "EXP_FINAL", "- ( EXP )"],"-": ["r", "EXP_FINAL", "- ( EXP )"], "*": ["r", "EXP_FINAL", "- ( EXP )"],"/": ["r", "EXP_FINAL", "- ( EXP )"], "%": ["r", "EXP_FINAL", "- ( EXP )"]}
    table.append(q176)
    q177 = {"fim": ["r", "BLOCO_ENQUANTO", "enquanto EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim"],"id": ["r", "BLOCO_ENQUANTO", "enquanto EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim"],"receba": ["r", "BLOCO_ENQUANTO", "enquanto EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim"],"escreva": ["r", "BLOCO_ENQUANTO", "enquanto EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim"],"leia": ["r", "BLOCO_ENQUANTO", "enquanto EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim"],"para": ["r", "BLOCO_ENQUANTO", "enquanto EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim"],"enquanto": ["r", "BLOCO_ENQUANTO", "enquanto EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim"],"se": ["r", "BLOCO_ENQUANTO", "enquanto EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim"],"pare": ["r", "BLOCO_ENQUANTO", "enquanto EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim"]}
    table.append(q177)
    q178 = {"id": ["r", "SINAL", "ε"], "(": ["s", 95], "-": ["s", 87], "numero_inteiro": ["r", "SINAL", "ε"],"numero_real": ["r", "SINAL", "ε"], "EXP": ["d", 184], "EXP_N2": ["d", 83], "EXP_N3": ["d", 84],"EXP_FINAL": ["d", 85], "SINAL": ["d", 86]}
    table.append(q178)
    q179 = {"ponto": ["r", "CONCATENAR_LEIA", "id [ EXP ]"], ";": ["s", 185]}
    table.append(q179)
    q180 = {")": ["r", "PARAMETROS", "VETOR TIPO : id ; PARAMETROS"]}
    table.append(q180)
    q181 = {"fim": ["r", "BLOCO_IF", "se EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim BLOCO_SENAO"],"id": ["r", "BLOCO_IF", "se EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim BLOCO_SENAO"],"receba": ["r", "BLOCO_IF", "se EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim BLOCO_SENAO"],"escreva": ["r", "BLOCO_IF", "se EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim BLOCO_SENAO"],"leia": ["r", "BLOCO_IF", "se EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim BLOCO_SENAO"],"para": ["r", "BLOCO_IF", "se EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim BLOCO_SENAO"],"enquanto": ["r", "BLOCO_IF", "se EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim BLOCO_SENAO"],"se": ["r", "BLOCO_IF", "se EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim BLOCO_SENAO"],"pare": ["r", "BLOCO_IF", "se EXP_RELACIONAL_TOTAL inicio BLOCO_COMANDO fim BLOCO_SENAO"]}
    table.append(q181)
    q182 = {"inicio": ["s", 186]}
    table.append(q182)
    q183 = {"inicio": ["r", "EXP_FINAL", "SINAL id [ EXP ]"], "ponto": ["r", "EXP_FINAL", "SINAL id [ EXP ]"],")": ["r", "EXP_FINAL", "SINAL id [ EXP ]"], ";": ["r", "EXP_FINAL", "SINAL id [ EXP ]"],"]": ["r", "EXP_FINAL", "SINAL id [ EXP ]"], "ateh": ["r", "EXP_FINAL", "SINAL id [ EXP ]"],"or": ["r", "EXP_FINAL", "SINAL id [ EXP ]"], "&": ["r", "EXP_FINAL", "SINAL id [ EXP ]"],"=": ["r", "EXP_FINAL", "SINAL id [ EXP ]"], "<": ["r", "EXP_FINAL", "SINAL id [ EXP ]"],"<=": ["r", "EXP_FINAL", "SINAL id [ EXP ]"], ">": ["r", "EXP_FINAL", "SINAL id [ EXP ]"],">=": ["r", "EXP_FINAL", "SINAL id [ EXP ]"], "<>": ["r", "EXP_FINAL", "SINAL id [ EXP ]"],"**": ["r", "EXP_FINAL", "SINAL id [ EXP ]"], "+": ["r", "EXP_FINAL", "SINAL id [ EXP ]"],"-": ["r", "EXP_FINAL", "SINAL id [ EXP ]"], "*": ["r", "EXP_FINAL", "SINAL id [ EXP ]"],"/": ["r", "EXP_FINAL", "SINAL id [ EXP ]"], "%": ["r", "EXP_FINAL", "SINAL id [ EXP ]"]}
    table.append(q183)
    q184 = {"inicio": ["s", 187]}
    table.append(q184)
    q185 = {"id": ["s", 91], "CONCATENAR_LEIA": ["d", 188]}
    table.append(q185)
    q186 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 189], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q186)
    q187 = {"fim": ["r", "BLOCO_COMANDO", "ε"], "id": ["s", 52], "receba": ["s", 58], "escreva": ["s", 57],"leia": ["s", 56], "para": ["s", 55], "enquanto": ["s", 54], "se": ["s", 53], "pare": ["s", 50],"BLOCO_COMANDO": ["d", 190], "RECEBA": ["d", 51], "ESCREVA": ["d", 49], "LEIA": ["d", 48],"BLOCO_ATEH": ["d", 47], "BLOCO_ENQUANTO": ["d", 46], "BLOCO_IF": ["d", 45], "CHAMADA_FUNC": ["d", 43],"ATRIBUICAO": ["d", 44]}
    table.append(q187)
    q188 = {"ponto": ["r", "CONCATENAR_LEIA", "id [ EXP ] ; CONCATENAR_LEIA"]}
    table.append(q188)
    q189 = {"fim": ["s", 191]}
    table.append(q189)
    q190 = {"fim": ["s", 192]}
    table.append(q190)
    q191 = {"fim": ["r", "BLOCO_SENAO", "senao inicio BLOCO_COMANDO fim"],"id": ["r", "BLOCO_SENAO", "senao inicio BLOCO_COMANDO fim"],"receba": ["r", "BLOCO_SENAO", "senao inicio BLOCO_COMANDO fim"],"escreva": ["r", "BLOCO_SENAO", "senao inicio BLOCO_COMANDO fim"],"leia": ["r", "BLOCO_SENAO", "senao inicio BLOCO_COMANDO fim"],"para": ["r", "BLOCO_SENAO", "senao inicio BLOCO_COMANDO fim"],"enquanto": ["r", "BLOCO_SENAO", "senao inicio BLOCO_COMANDO fim"],"se": ["r", "BLOCO_SENAO", "senao inicio BLOCO_COMANDO fim"],"pare": ["r", "BLOCO_SENAO", "senao inicio BLOCO_COMANDO fim"]}
    table.append(q191)
    q192 = {"fim": ["r", "BLOCO_ATEH", "para id de EXP ateh EXP inicio BLOCO_COMANDO fim"],"id": ["r", "BLOCO_ATEH", "para id de EXP ateh EXP inicio BLOCO_COMANDO fim"],"receba": ["r", "BLOCO_ATEH", "para id de EXP ateh EXP inicio BLOCO_COMANDO fim"],"escreva": ["r", "BLOCO_ATEH", "para id de EXP ateh EXP inicio BLOCO_COMANDO fim"],"leia": ["r", "BLOCO_ATEH", "para id de EXP ateh EXP inicio BLOCO_COMANDO fim"],"para": ["r", "BLOCO_ATEH", "para id de EXP ateh EXP inicio BLOCO_COMANDO fim"],"enquanto": ["r", "BLOCO_ATEH", "para id de EXP ateh EXP inicio BLOCO_COMANDO fim"],"se": ["r", "BLOCO_ATEH", "para id de EXP ateh EXP inicio BLOCO_COMANDO fim"],"pare": ["r", "BLOCO_ATEH", "para id de EXP ateh EXP inicio BLOCO_COMANDO fim"]}
    table.append(q192)

    return table
############################################
# ANALIZADOR SINTATICO - FIM
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
    global  TOKENS
    input_str = sys.stdin.read()
    programa = processadorLinhas(input_str)
    if LEXICA_CORRETA:
        q0(programa)
        newToken = Token("$", "$")
        TOKENS.append(newToken)
        tabela = preencherTable()
        isCorrect = analisadorSintatico(TOKENS,tabela)
    if isCorrect:
        print("YES")
    else:
        print("NO")
############################################
# FIM MAIN
############################################
main()