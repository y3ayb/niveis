from random import random, shuffle, gauss
from enum import Enum
from copy import deepcopy

class Color(Enum):
    RED = 1
    YELLOW = 2
    BLUE = 3

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

class Move:
    def __init__ (self, loc, dir):
        self.loc = loc
        self.dir = dir

class Arrow:
    def __init__(self, w, d, s, a):
        self.w = w
        self.d = d
        self.s = s
        self.a = a

def createPossibilities():
    A = []
    for i in range(25): A.append(Arrow(False, False, False, False))
    A.append(0)
    return A

def createTable():
    A = [Block(1,Color.YELLOW),Block(1,Color.YELLOW),Block(1,Color.YELLOW),Block(1,Color.YELLOW),Block(1,Color.YELLOW)]
    A.extend([Block(1,Color.YELLOW),Block(1,Color.YELLOW),Block(1,Color.YELLOW),Block(1,Color.YELLOW),Block(1,Color.YELLOW)])
    A.extend([Block(1,Color.BLUE),Block(1,Color.BLUE),Block(1,Color.BLUE),Block(1,Color.BLUE),Block(1,Color.BLUE)])
    A.extend([Block(1,Color.BLUE),Block(1,Color.BLUE),Block(1,Color.BLUE),Block(1,Color.BLUE),Block(1,Color.RED)])
    A.extend([Block(1,Color.RED),Block(1,Color.RED),Block(1,Color.RED),Block(2,Color.RED),Block(2,Color.RED)])
    shuffle(A)
    return A

def countColorTable(A):
    b=0
    r=0
    for i in range(25):
        if A[i].color==Color.BLUE: b=b+1
        elif A[i].color==Color.RED: r=r+1
    return [b,r,25-b-r]

def printTable(A):
    for i in range(2): print(A[5*i],A[5*i+1],A[5*i+2],A[5*i+3],A[5*i+4],' ',' '+str(5*i),' '+str(5*i+1),' '+str(5*i+2),' '+str(5*i+3),' '+str(5*i+4))
    for i in range(2,5): print(A[5*i],A[5*i+1],A[5*i+2],A[5*i+3],A[5*i+4],' ',str(5*i),str(5*i+1),str(5*i+2),str(5*i+3),str(5*i+4))  
    print()

def findMoves (A):
    psb = createPossibilities()
    for i in range(25):
        if A[i].color == Color.BLUE:
            if i-5>=0:
                if (A[i-5].color==Color.BLUE and A[i].value==A[i-5].value) or (A[i-5].color!=Color.BLUE and A[i].value>=A[i-5].value):
                    psb[i].w = True
                    psb[25] = psb[25]+1
            if i%5!=4:
                if (A[i+1].color==Color.BLUE and A[i].value==A[i+1].value) or (A[i+1].color!=Color.BLUE and A[i].value>=A[i+1].value):
                    psb[i].d = True
                    psb[25] = psb[25]+1
            if i+5<=24:
                if (A[i+5].color==Color.BLUE and A[i].value==A[i+5].value) or (A[i+5].color!=Color.BLUE and A[i].value>=A[i+5].value):
                    psb[i].s = True
                    psb[25] = psb[25]+1
            if i%5!=0:
                if (A[i-1].color==Color.BLUE and A[i].value==A[i-1].value) or (A[i-1].color!=Color.BLUE and A[i].value>=A[i-1].value):
                    psb[i].a = True
                    psb[25] = psb[25]+1
        elif A[i].color == Color.YELLOW:
            if i-5>=0:
                if A[i-5].color==Color.YELLOW and A[i].value==A[i-5].value:
                    psb[i].w = True
                    psb[25] = psb[25]+1
            if i%5!=4:
                if A[i+1].color==Color.YELLOW and A[i].value==A[i+1].value:
                    psb[i].d = True
                    psb[25] = psb[25]+1
            if i+5<=24:
                if A[i+5].color==Color.YELLOW and A[i].value==A[i+5].value:
                    psb[i].s = True
                    psb[25] = psb[25]+1
            if i%5!=0:
                if A[i-1].color==Color.YELLOW and A[i].value==A[i-1].value:
                    psb[i].a = True
                    psb[25] = psb[25]+1
    return psb

def printMoves (psb):
    for i in range(25):
        if psb[i].w == True or psb[i].d == True or psb[i].s == True or psb[i].a == True:
            print(i, end=' ')
            if psb[i].w == True: print('w', end=' ')
            if psb[i].d == True: print('d', end=' ')
            if psb[i].s == True: print('s', end=' ')
            if psb[i].a == True: print('a', end=' ')                                
    print()

def increaseLevel (qmove):
    inc = 1.45/(qmove+9)+0.6/((qmove+9)**2)
    return inc

def sortBlock (lvl):
    a = random()
    if a <= 0.4: block = Block(1, Color.BLUE)
    elif a <= 0.8: block = Block(1, Color.YELLOW)
    else:
        b = int(gauss(lvl,0.166))+1
        #b = int((lvl+random()*lvl)/2)+1
        block = Block(b, Color.RED)
    return block 

def moveUp (lvl, move, A0):
    A = deepcopy(A0)
    aux = A[move.loc]
    if A[move.loc-5].color == A[move.loc].color: aux.value = aux.value + 1
    if move.loc//5 != 4:
        for i in range(4-move.loc//5): A[5*(i+move.loc//5)+move.loc%5] = A[5*(i+1+move.loc//5)+move.loc%5]
    A[move.loc%5+20] = sortBlock(lvl)
    A[move.loc-5] = aux
    return A

def moveLeft (lvl, move, A0):
    A = deepcopy(A0)
    aux = A[move.loc]
    if A[move.loc+1].color == A[move.loc].color: aux.value = aux.value + 1
    if move.loc%5 != 0:
        for i in range(move.loc%5): A[5*(move.loc//5)+move.loc%5-i] = A[5*(move.loc//5)+move.loc%5-i-1]
    A[5*(move.loc//5)] = sortBlock(lvl)
    A[move.loc+1] = aux
    return A

def moveDown (lvl, move, A0):
    A = deepcopy(A0)
    aux = A[move.loc]
    if A[move.loc+5].color == A[move.loc].color:
        aux.value = aux.value + 1
    if move.loc//5 != 0:
        for i in range(move.loc//5): A[5*(-i+move.loc//5)+move.loc%5] = A[5*(-1-i+move.loc//5)+move.loc%5]
    A[move.loc%5] = sortBlock(lvl)
    A[move.loc+5] = aux
    return A

def moveRight (lvl, move, A0):
    A = deepcopy(A0)
    aux = A[move.loc]
    if A[move.loc-1].color == A[move.loc].color:
        aux.value = aux.value + 1
    if move.loc%5 != 4:
        for i in range(4-move.loc%5): A[5*(move.loc//5)+move.loc%5+i] = A[5*(move.loc//5)+move.loc%5+i+1]
    A[5*(move.loc//5)+4] = sortBlock(lvl)
    A[move.loc-1] = aux
    return A

def modTable (lvl, move, A0):
    if move.dir == 'w': A = moveUp(lvl, move, A0)
    if move.dir == 'd': A = moveLeft(lvl, move, A0)
    if move.dir == 's': A = moveDown(lvl, move, A0)
    if move.dir == 'a': A = moveRight(lvl, move, A0)            
    return A
