import bib
import ui

def inputDir ():
    dir = input('Direção: ')
    while dir != 'w' and dir != 'd' and dir != 's' and dir != 'a': dir = input('Direção(W, D, S ou A): ')
    return dir

def inputInt ():
    loc = input('Posição: ')
    while loc != '0' and loc != '1' and loc != '2' and loc != '3' and loc != '4' and loc != '5' and loc != '6' and loc != '7' and loc != '8' and loc != '9' and loc != '10' and loc != '11' and loc != '12' and loc != '13' and loc != '14' and loc != '15' and loc != '16' and loc != '17' and loc != '18' and loc != '19' and loc != '20' and loc != '21' and loc != '22' and loc != '23' and loc != '24':
        loc = input('Posição (0 à 24): ')
    loc = int(loc)
    return loc

def inputMove (psb):
    a = False
    move = bib.Move(0,'w')
    while a == False:
        a = True            
        move.loc = inputInt()
        move.dir = inputDir()
        if (move.dir == 'w' and psb[move.loc].w == False) or (move.dir == 'd' and psb[move.loc].d == False) or (move.dir == 's' and psb[move.loc].s == False) or (move.dir == 'a' and psb[move.loc].a == False):
            a = False
            print('Movimento Impossível') 
            bib.printMoves(psb)
            print()
    return move

def inputMode ():
    psb = bib.createPossibilities()
    A = bib.createTable()
    qmove = 0
    lvl = 2
    print(qmove, lvl)
    bib.printTable(A)
    psb = bib.findMoves(A)
    bib.printMoves(psb)
    print(psb[25])
    print()
    move = bib.Move(1,'w')
    while (psb[25]!=0):
        qmove = qmove + 1
        lvl = lvl + bib.increaseLevel(qmove)
        move = inputMove(psb)
        A = bib.modTable(lvl, move, A)
        print(qmove, lvl)
        bib.printTable(A)
        psb = bib.findMoves(A)
        bib.printMoves(psb)
        print(psb[25])
        print()
    print('Game Over')
    
def inputModeGraf ():
    psb = bib.createPossibilities()
    A = bib.createTable()
    qmove = 0
    lvl = 2
    psb = bib.findMoves(A)
    print()
    ui.printTableInput(A,qmove)
    move = bib.Move(1,'w')
    while (psb[25]!=0):
        qmove = qmove + 1
        lvl = lvl + bib.increaseLevel(qmove)
        move = inputMove(psb)
        A = bib.modTable(lvl, move, A)
        psb = bib.findMoves(A)
        print()
        ui.printTableInput(A, qmove)
    print('Game Over')
