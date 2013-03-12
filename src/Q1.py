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
import tkMessageBox
import sys


###############################################################################
#CLASS
###############################################################################

###############################################################################
#GameSquare
###############################################################################
# The GameSquare object
###############################################################################
class GameSquare:
    def __init__(self, legend, hasPlayer):
        self.hasPlayer = hasPlayer
        if(legend == 'E'):
            self.legend = []
        else:
            self.legend = [legend]
        self.string = StringVar()
        self.reload()
        self.backgroundColor = 'black'
        if(self.hasPlayer):
            self.backgroundColor = 'white'

    def getLegend(self):
        return self.legend

    def label(self, master):
        self.l = Label(
            master,
            textvariable = self.string,
            background = self.backgroundColor,
            width = 10,
            height = 5
        )
        return self.l

    def reload(self):
        self.string.set(self)

    def __str__(self):
        returnString = ''.join(self.legend)
        if(self.hasPlayer):
            returnString +=  "\n"
            returnString += "o\n"
            returnString += "/|\\\n"
            returnString += "/ \\\n"

        # elif(self.legend == 'W'):
        #     returnString +=  "\n"
        #     returnString+= "  ^o^\n"
        #     returnString+= "^\/0\/^\n"
        #     returnString+= "  /O\\\n"
        #     returnString+= "_| /_"
        return returnString

###############################################################################
#GameBoard
###############################################################################
# The GameSquare object
###############################################################################
class GameBoard:
    def keyPress(self, event):
        key = event.keysym
        x,y = self.playerPos
        newX,newY = x,y

        if("Up" == key):
            #If we hit the top, dont keep going.
            if(x == 0):
                return
            newX -= 1
            
        elif("Down" == key):
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
        elif("space" == key):
            legend = self.GameSquareMasterList[x][y].getLegend()
            if('S' == legend):
                exit()
            elif('G' == legend):
                self.GameSquareMasterList[x][y].legend.remove('G')
                self.GameSquareMasterList[x][y].reload()
            return

        self.playerPos = (newX,newY)

        #Set the new player pos
        self.GameSquareMasterList[x][y].hasPlayer = False
        self.GameSquareMasterList[x][y].l.configure(background='white')

        self.GameSquareMasterList[newX][newY].hasPlayer = True
        self.GameSquareMasterList[newX][newY].l.configure(background='white')


        #Redraw
        self.GameSquareMasterList[x][y].reload()
        self.GameSquareMasterList[newX][newY].reload()

    def __init__(self, textBoard):
        self.playerPos = None
        master = Tk()

        master.bind("<Key>", self.keyPress)
        master.title("Wumpus' Dungeon")
        self.SIZE = int(textBoard.pop(0))
        itemLocations = {
            'G':[],
            'P':[],
            'W':[]
        }

        GameSquareMasterList = list()
        for x in range(self.SIZE):

            GameSquareList = list()
            for y in range(self.SIZE):

                item = textBoard[x][y]

                hasPlayer = False
                if(item == 'S'):
                    hasPlayer = True
                    self.playerPos = (x,y)
                elif(not item == 'E' ):
                    itemLocations[item].append((x,y))

                gs = GameSquare(item, hasPlayer)
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
        self.addWarnings(itemLocations)

    def addWarnings(self, itemLocations):
        for item in itemLocations:
            print item

            for x,y in itemLocations[item]:
                warning = ''
                if('P' == item):
                    warning = 'B'
                elif('W' == item):
                    warning = 'S'
                #elif('G' == item):
                #    print 'G'
                else:
                    continue
                for newX in range(x-1, x+1):
                    if(newX<0 or newX>self.SIZE-1):
                        continue
                    for newY in range(y-1, y+1):
                        if(newY<0 or newY>self.SIZE-1):
                            continue
                        print warning, newX, newY
                        if(newY != Y and newX != X and warning not in self.GameSquareMasterList):
                            self.GameSquareMasterList[newX][newY].legend.append(warning)
                            self.GameSquareMasterList[newX][newY].reload()

    def loop(self):
        self.master.mainloop() 

###############################################################################
#FUNCTIONS
###############################################################################

fileLoc = sys.argv[1]
f = open(fileLoc, 'r')

file = f.read().strip().split("\n")

gb = GameBoard(list(file))

tkMessageBox.showinfo(
    "How To Play", 
    "Arrow keys to move\n"+
    "Space to leave\n"+
    ""
)

gb.loop()
