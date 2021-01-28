from random import random, shuffle, gauss
from enum import Enum
from copy import deepcopy

#As cores possíveis de cada bloco
class Color(Enum):
    RED = 1
    YELLOW = 2
    BLUE = 3

#Cada peça do jogo tem um valor(número) e uma cor
class Block:
    def __init__ (self, value, color):
        self.value = value
        self.color = color
    def __repr__(self):
        if self.color == Color.RED:
            return str(self.value)+' RED '
        if self.color == Color.BLUE:
            return str(self.value)+' BLU '
        if self.color == Color.YELLOW:
            return str(self.value)+' YEL '

#No app orginal, o movimento é feito selecionando um bloco (com o dedo) e empurrando para alguma direção. Logo o movimento tem um posição (loc) e uma direção (dir)
class Move:
    def __init__ (self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

#O movimento precisa de uma direção. Aqui são definidas essas direção: w é cima, d é direita, s é baixo, a é esquerda. Essa estrutura será usada no movimento do bloco, principalmente pela rede neural
class Arrow:
    def __init__(self, w, d, s, a):
        self.w = w
        self.d = d
        self.s = s
        self.a = a

#O tabuleiro tab é uma matriz 5x5 de block, enquanto a quantidade de movimentos é nmove e o nível é lvl.
class Board:
    def __init__ (self, tab, nmove, lvl):
        self.tab = tab
        self.nmove = nmove
        self.lvl = lvl

#As possibilidades de movimento psb é uma matriz 5x5 de arrow, enaquanto a quantidade de movimentos possíveis é npsb
class Possibilities:
    def __init__ (self, psb, npsb):
        self.psb = psb
        self.npsb = npsb
        
'''O tabuleiro é composto por 25 blocos (5x5).
Inicialmente são 10 blocos amarelos nivel 1, 9 blocos azuis nível 1, 4 blocos vermelhos nível 1 e 2 blocos vermelhos nível 2, que são embaralhados.
A mesa ainda não tem movimentos e o nível inicial é 2.'''
def createBoard():
    A = [Block(1,Color.YELLOW),Block(1,Color.YELLOW),Block(1,Color.YELLOW),Block(1,Color.YELLOW),Block(1,Color.YELLOW)]
    A.extend([Block(1,Color.YELLOW),Block(1,Color.YELLOW),Block(1,Color.YELLOW),Block(1,Color.YELLOW),Block(1,Color.YELLOW)])
    A.extend([Block(1,Color.BLUE),Block(1,Color.BLUE),Block(1,Color.BLUE),Block(1,Color.BLUE),Block(1,Color.BLUE)])
    A.extend([Block(1,Color.BLUE),Block(1,Color.BLUE),Block(1,Color.BLUE),Block(1,Color.BLUE),Block(1,Color.RED)])
    A.extend([Block(1,Color.RED),Block(1,Color.RED),Block(1,Color.RED),Block(2,Color.RED),Block(2,Color.RED)])
    shuffle(A)
    B = Board([], 0, 2)
    for i in range (5):
        B.tab.append([])
        for j in range (5): B.tab[i].append(A[5*i+j])
    return B

'''Essa é uma matriz de arrow com os movimentos possíveis. Lembrando que o movimento tem uma posição e uma direção.
Inicialmente nenhum movimento é possível, logo a quantidade de movimentos possíveis npsb inicialmente é 0.'''
def createPossibilities():
    A = Possibilities([], 0)
    for i in range(5): 
        A.psb.append([])
        for j in range (5): A.psb[i].append(Arrow(False, False, False, False))
    return A

'''Checa se um movimento é possível.
Blocos azuis podem se movimentar em direção de outro bloco azul, desde que tenha o mesmo valor ou em direção de um bloco com cor diferente, desde que tenha um valor maior.
Blocos amarelos podem se movimentar em direção de outro bloco amarelo com o mesmo valor.'''
def moveIsPossible (blockSelected, blockNeighbor):
    if blockSelected.color == Color.BLUE:
        if blockNeighbor.color == Color.BLUE and blockNeighbor.value == blockSelected.value: psb = True
        elif blockNeighbor.color != Color.BLUE and blockNeighbor.value <= blockSelected.value: psb = True
        else: psb = False
    elif blockSelected.color == Color.YELLOW:
        if blockNeighbor.color == Color.YELLOW and blockNeighbor.value == blockSelected.value: psb = True
        else: psb = False
    else: psb = False
    return psb

#Verifica os movimentos possíveis
def findMoves (A):
    p = createPossibilities()
    for i in range (4):
        for j in range (5):
            p.psb[i+1][j].w = moveIsPossible(A.tab[i+1][j], A.tab[i][j]) #Movimento para cima
            if p.psb[i+1][j].w == True: p.npsb = p.npsb + 1
            p.psb[j][i].d = moveIsPossible(A.tab[j][i], A.tab[j][i+1]) #Movimento para direita
            if p.psb[j][i].d == True: p.npsb = p.npsb + 1
            p.psb[i][j].s = moveIsPossible(A.tab[i][j], A.tab[i+1][j]) #Movimento para baixo
            if p.psb[i][j].s == True: p.npsb = p.npsb + 1
            p.psb[j][i+1].a = moveIsPossible(A.tab[j][i+1], A.tab[j][i]) #Movimento para esquerda
            if p.psb[j][i+1].a == True: p.npsb = p.npsb + 1
    return p

#O incremento do nível é essa função louca sem muito sentido. É o que tenho pra hoje.
def increaseLevel (nmove):
    x = 1.45/(nmove+9)+0.6/((nmove+9)**2)
    return x

'''Função que escolhe o novo bloco que aparece no tabuleiro. 
Tem 40% de chance de ser um bloco azul (nível 1), 40% de chance de ser um bloco amarelo (nível 1) e 20% de chance de ser um bloco vermelho.
O nível do bloco vermelho é escolhido por essa função louca que não tem muita explicação'''
def sortBlock (lvl):
    a = random()
    if a <= 0.4: block = Block(1, Color.BLUE)
    elif a <= 0.8: block = Block(1, Color.YELLOW)
    else:
        b = int(gauss(lvl,0.166))+1
        #b = int((lvl+random()*lvl)/2)+1
        block = Block(b, Color.RED)
    return block 

#Realiza o movimento para cima. Retorna uma matriz 5x5 de blocos
def moveUp (move, A0, lvl):
    A = deepcopy(A0)
    aux = A[move.x][move.y]
    if A[move.x-1][move.y].color == A[move.x][move.y].color: aux.value = aux.value + 1
    if move.x != 4:
        for i in range (4 - move.x): A[i+move.x][move.y] = A[i+1+move.x][move.y]
    A[4][move.y] = sortBlock(lvl)
    A[move.x-1][move.y] = aux
    return A

#Realiza o movimento para direita. Retorna uma matriz 5x5 de blocos
def moveRight (move, A0, lvl):
    A = deepcopy(A0)
    aux = A[move.x][move.y]
    if A[move.x][move.y+1].color == A[move.x][move.y].color: aux.value = aux.value + 1
    if move.y != 0:
        for i in range (move.y): A[move.x][move.y-i] = A[move.x][move.y-i-1]
    A[move.x][0] = sortBlock(lvl)
    A[move.x][move.y+1] = aux
    return A

#Realiza o movimento para baixo. Retorna uma matriz 5x5 de blocos
def moveDown (move, A0, lvl):
    A = deepcopy(A0)
    aux = A[move.x][move.y]
    if A[move.x+1][move.y].color == A[move.x][move.y].color: aux.value = aux.value + 1
    if move.x != 0:
        for i in range (move.x): A[move.x-i][move.y] = A[move.x-i-1][move.y]
    A[0][move.y] = sortBlock(lvl)
    A[move.x+1][move.y] = aux
    return A

#Realiza o movimento para esquerda. Retorna uma matriz 5x5 de blocos
def moveLeft (move, A0, lvl):
    A = deepcopy(A0)
    aux = A[move.x][move.y]
    if A[move.x][move.y-1].color == A[move.x][move.y].color: aux.value = aux.value + 1
    if move.y != 4:
        for i in range(4 - move.y): A[move.x][move.y+i] = A[move.x][move.y+i+1]
    A[move.x][4] = sortBlock(lvl)
    A[move.x][move.y-1] = aux
    return A

#Realiza o movimento no tabuleiro
def modBoard (move, A0):
    A = deepcopy(A0)
    A.nmove = A.nmove + 1
    A.lvl = A.lvl + increaseLevel(A.nmove)
    if move.dir == 'w': A.tab = moveUp(move, A0.tab, A0.lvl)
    if move.dir == 'd': A.tab = moveRight(move, A0.tab, A0.lvl)
    if move.dir == 's': A.tab = moveDown(move, A0.tab, A0.lvl)
    if move.dir == 'a': A.tab = moveLeft(move, A0.tab, A0.lvl)            
    return A
