import bib
import uibib as uibib

def selectMove (i, j, dir, ui):
    global M
    M = bib.Move(i, j, dir)
    ui.destroy()

def buttonPrint(ui, p, dir, i, j):
    txt = uibib.Button(ui, text=dir)
    if (p == False): txt["state"] = uibib.DISABLED
    else: txt["command"] = lambda: selectMove (i, j, dir, ui)
    if dir == 'w': txt.place(x=50+120*j, y=45+120*i, width=30, height=30)
    elif dir == 'd': txt.place(x=85+120*j, y=80+120*i, width=30, height=30)
    elif dir == 's': txt.place(x=50+120*j, y=115+120*i, width=30, height=30)
    else: txt.place(x=15+120*j, y=80+120*i, width=30, height=30)

'''def buttonUpPrint(ui, P, i, j):
    txt = uibib.Button(ui, text='w')
    if (P.psb[i][j].w == False): txt["state"] = uibib.DISABLED
    else: txt["command"] = lambda: selectMove (i, j, 'w', ui)
    txt.place(x=50+120*j, y=45+120*i, width=30, height=30)

def buttonRightPrint(ui, P, i, j):
    if (P.psb[i][j].d == False): txt = uibib.Label(ui)
    else: txt = uibib.Button(ui, text='d', command = lambda: selectMove (i, j, 'd', ui))
    txt.place(x=85+120*j, y=80+120*i, width=30, height=30)

def buttonDownPrint(ui, P, i, j):
    if (P.psb[i][j].s == False): txt = uibib.Label(ui)
    else: txt = uibib.Button(ui, text='s', command = lambda: selectMove (i, j, 's', ui))
    txt.place(x=50+120*j, y=115+120*i, width=30, height=30)

def buttonLeftPrint(ui, P, i, j):
    if (P.psb[i][j].a == False): txt = uibib.Label(ui)
    else: txt = uibib.Button(ui, text='a', command = lambda: selectMove (i, j, 'a', ui))
    txt.place(x=15+120*j, y=80+120*i, width=30, height=30)'''

def printBoard (A, P):
    ui = uibib.head()
    uibib.numberMoves(ui, A.nmove)
    for i in range (5):
        for j in range (5): 
            uibib.blockPrint(ui, A.tab[i][j], i, j)
            buttonPrint(ui, P.psb[i][j].w, 'w', i, j)
            buttonPrint(ui, P.psb[i][j].d, 'd', i, j)
            buttonPrint(ui, P.psb[i][j].s, 's', i, j)
            buttonPrint(ui, P.psb[i][j].a, 'a', i, j)
    ui.mainloop()

def inputMode ():
    A = bib.createBoard()
    P = bib.findMoves(A)
    global M
    M = bib.Move(0, 0, 'exit')
    while (P.npsb != 0):
        printBoard (A, P)
        if M.dir == 'exit': exit ()
        else: 
            A = bib.modBoard(M, A)
            P = bib.findMoves(A)
            M.dir = 'exit'
    uibib.printGameOver(A)
