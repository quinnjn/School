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

class GameSquare:
    def __init__(self, legend, hasPlayer):
        self.hasPlayer = hasPlayer
        self.legend = legend
        self.string = StringVar()
        self.setString(self)

    def getLegend(self):
        return self.legend

    def label(self, master):
        self.l = Label(
            master,
            textvariable = self.string,
            width = 10,
            height = 5
        )
        return self.l

    def reload(self):
        self.setString(self)

    def setString(self, string):
        self.string.set(string)

    def __str__(self):
        returnString = self.legend
        if(self.hasPlayer):
            returnString +=  "\n"
            returnString += "o\n"
            returnString += "/|\\\n"
            returnString += "/ \\\n"
                # "o\n"+=
                # "+\n"+=
                # "/\\"
        return returnString

class GameBoard:
    def keyPress(self, event):
        key = event.keysym
        print self.playerPos
        x,y = self.playerPos
        newX,newY = x,y

        if(key == "Up"):
            #If we hit the top, dont keep going.
            if(x == 0):
                return
            newX -= 1
            
        elif(key == "Down"):
            #If we are at SIZE, dont keep going.
            if(x == self.SIZE-1):
                return
            newX += 1

        elif("Left" == key):
            if(y == 0):
                return
            newY -= 1
        elif("Right" == key):
            if(y == self.SIZE-1):
                return
            newY += 1

        self.playerPos = (newX,newY)

        #Set the new player pos
        self.GameSquareMasterList[x][y].hasPlayer = False
        self.GameSquareMasterList[newX][newY].hasPlayer = True

        #Redraw
        self.GameSquareMasterList[x][y].reload()
        self.GameSquareMasterList[newX][newY].reload()

        self.master.update_idletasks()

    def __init__(self, textBoard):
        self.playerPos = False
        master = Tk()
        master.bind("<Key>", self.keyPress)
        master.title("Wumpus' Dungeon")
        self.SIZE = int(textBoard.pop(0))

        print textBoard

        GameSquareMasterList = list()
        for x in range(self.SIZE):

            GameSquareList = list()
            for y in range(self.SIZE):

                hasPlayer = False
                if(textBoard[x][y] == 'S'):
                    hasPlayer = True
                    self.playerPos = (x,y)
                gs = GameSquare(textBoard[x][y], hasPlayer)
                GameSquareList.append(gs)

                gs.label(
                    master
                ).grid(
                    row=x, 
                    column=y
                )       

            GameSquareMasterList.append(GameSquareList)
        self.master = master
        self.GameSquareMasterList = GameSquareMasterList


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
