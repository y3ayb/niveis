import bib
from tkinter import *

def printMoves (p):
    for i in range(5):
        for j in range (5):
            if p.psb[i][j].w == True or p.psb[i][j].d == True or p.psb[i][j].s == True or p.psb[i][j].a == True:
                print(str(i)+'x'+str(j), end=' ')
                if p.psb[i][j].w == True: print('w', end=' ')
                if p.psb[i][j].d == True: print('d', end=' ')
                if p.psb[i][j].s == True: print('s', end=' ')
                if p.psb[i][j].a == True: print('a', end=' ')                                
    print()

def head ():
    jogo = Tk()
    jogo.title("Níveis")
    jogo.geometry("610x640")
    return jogo

def numberMoves (ui, n):
    txt = Label(ui, text=str(n))
    txt.place(x=10, y=10, width=40, height=20)

def gameOver (ui, n):
    txt = Label(ui, text='Game Over! O jogo teve '+str(n)+' movimentos')
    txt["font"] = ("Calibri", "12", "bold")
    txt.place(x=10, y=10, width=400, height=20)

def blockPrint (ui, block, i, j):
    txt = Label(ui, text = str(block.value), bg="blue")
    if block.color == bib.Color.YELLOW: txt["bg"] = ("yellow")
    elif block.color == bib.Color.BLUE: txt["fg"] = ("white")
    else: txt["bg"] = ("red")
    txt["font"] = ("Calibri", "16", "bold")
    txt.place(x=10+120*j, y=40+120*i, width=110, height=110)

def buttonExit (ui):
    txt = Button(ui, text='Sair', command = exit)
    txt.place(x=550, y=10, width=50, height=20)

def printGameOver (A):
    ui = head()
    gameOver(ui, A.nmove)
    buttonExit(ui)
    for i in range (5):
        for j in range (5): blockPrint(ui, A.tab[i][j], i, j)
    ui.mainloop()
