###############################################################################
#Q1.py 
#CMPT 317 A3
#Quinn Neumiiller
#11065618
#qjn162
###############################################################################
#IMPORTS
###############################################################################
from Tkinter import *
import sys


###############################################################################
#CLASS
###############################################################################

class GameBoard:
    def __init__(self, textBoard):
        master = Tk()
        master.title("Wumpus' Dungeon")
        SIZE = int(textBoard.pop(0))

        print textBoard


        for x in range(SIZE):
            for y in range(SIZE):

                l = Label(
                    master,
                    text= textBoard[x][y] +"\n",
                    width=10,
                    height=5
                ).grid(
                    row=x, 
                    column=y
                )       
        self.master = master

    def loop(self):
        self.master.mainloop() 

###############################################################################
#FUNCTIONS
###############################################################################

fileLoc = sys.argv[1]
f = open(fileLoc, 'r')

file = f.read().strip().split("\n")

gb = GameBoard(list(file))
gb.loop()