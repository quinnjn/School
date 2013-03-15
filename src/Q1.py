# -*- coding: utf-8 -*- 
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
    ###################################################
    # Constructor
    ###################################################
    # Params:
    # legend - The items that this GameSquare will have
    # hasPlayer - Does this square currently hold the player?
    # playerArrowDirection - If there is a arrow, where is it pointing?
    ###################################################
    def __init__(self, legend, hasPlayer, playerArrowDirection):
        self.hasPlayer = hasPlayer
        self.playerArrowDirection = playerArrowDirection
        if(legend == 'E'):
            self.legend = []
        else:
            self.legend = [legend]
        self.string = StringVar()
        self.reload()
        self.backgroundColor = 'black'
        if(self.hasPlayer):
            self.backgroundColor = 'white'
    ###################################################
    # label
    ###################################################
    # Creates the label the GameSquare uses
    ###################################################
    # Params:
    # master - the master object to attach this gameSquare to
    ###################################################
    # Returns:
    # The GameSquares Label
    ###################################################

    def label(self, master):
        self.l = Label(
            master,
            textvariable = self.string,
            background = self.backgroundColor,
            width = 15,
            height = 5
        )
        return self.l
    ###################################################
    # getArrowDir
    ###################################################
    # Returns the arrow direction
    ###################################################
    # Returns:
    # Returns the arrow direction
    ###################################################
    def getArrowDir(self):
        return self.playerArrowDirection
    ###################################################
    # setArrowDir
    ###################################################
    # Sets the arrow direction 
    ###################################################
    # Params:
    # arrowDir - the direction the arrow should be set to.
    ###################################################
    def setArrowDir(self, arrowDir):
        self.playerArrowDirection = arrowDir

    ###################################################
    # reload
    ###################################################
    # Reloads the GameSquare
    ###################################################
    def reload(self):
        self.string.set(self)
    ###################################################
    # toString
    ###################################################
    def __str__(self):
        returnString = ', '.join(self.legend)
        returnString = returnString.replace('G', '☼')
        if(self.hasPlayer):
            returnString +=  "\n"
            returnString += "o\n"
            returnString += "/|\\"
            returnString += self.playerArrowDirection
            returnString += "\n"
            returnString += "/ \\\n"
        elif('S' in self.legend):
            returnString  = "|-|\n"
            returnString += "|-|\n"
            returnString += "|-|\n"

        return returnString

###############################################################################
#GameBoard
###############################################################################
# The GameSquare object
###############################################################################
class GameBoard:
    ###################################################
    #validRange
    ###################################################
    # Determines if a (x,y) are valid.
    ###################################################
    #Params:
    # x - x coord
    # y - y coord
    ###################################################
    #Returns:
    #True if valid, false otherwise.
    ###################################################
    def validRange(self,x,y):
        return ((x>=0 and x<self.SIZE)and(y>=0 and y<self.SIZE))
    ###################################################
    # shoot
    ###################################################
    # If a shoot happens, resolves it.    
    ###################################################
    # Params:
    # x - x coord
    # y - y coord
    ###################################################
    def shoot(self, x, y):
        if(not self.validRange(x,y)):
            return
        oldSquare = self.GameSquareMasterList[x][y]

        if('W' in oldSquare.legend):
            oldSquare.legend.remove('W')

            minX = x-1
            maxX = x+1
            minY = y-1
            maxY = y+1

            if(minX >= 0):
                self.GameSquareMasterList[minX][y].legend.remove('Smell')
                self.GameSquareMasterList[minX][y].reload()
            if(maxX < self.SIZE):
                self.GameSquareMasterList[maxX][y].legend.remove('Smell')
                self.GameSquareMasterList[maxX][y].reload()
            if(minY >= 0):
                self.GameSquareMasterList[x][minY].legend.remove('Smell')
                self.GameSquareMasterList[x][minY].reload()
            if(maxY < self.SIZE):
                self.GameSquareMasterList[x][maxY].legend.remove('Smell')
                self.GameSquareMasterList[x][maxY].reload()
    ###################################################
    # keyPress
    ###################################################
    # Accepts keyboard input and updates the game board
    # depending on the action recieved
    ###################################################
    # Params:
    # event - using this to grab the key pressed
    ###################################################

    def keyPress(self, event):
        key = event.keysym
        x,y = self.playerPos
        newX,newY = x,y

        oldSquare = self.GameSquareMasterList[x][y]

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
            #If we hit the left most side, dont keep going
            if(y == 0):
                return
            newY -= 1
        elif("Right" == key):
            #If we hit the right most side, dont keep going
            if(y == self.SIZE-1):
                return
            newY += 1
        elif("space" == key):
            #Action key is hit.
            legend = oldSquare.legend
            #If it's the start location, allow to exit.
            if('S' in legend):
                tkMessageBox.showinfo(
                    "LOST", 
                    "You left the dungeon but no gold :("
                )
                exit()
            #If it's the Gold location, allow to exit.
            elif('G' in legend):
                tkMessageBox.showinfo(
                    "WINNER", 
                    "You received the gold and left the dungeon!"
                )
                exit()
            return

        elif("w" == key and oldSquare.playerArrowDirection):
            oldSquare.playerArrowDirection = '↑'
        elif("a" == key and oldSquare.playerArrowDirection):
            oldSquare.playerArrowDirection = '←'
        elif("d" == key and oldSquare.playerArrowDirection):
            oldSquare.playerArrowDirection = '→'
        elif("s" == key and oldSquare.playerArrowDirection):
            oldSquare.playerArrowDirection = '↓'
        elif("q" == key and oldSquare.playerArrowDirection):
            arrow = oldSquare.playerArrowDirection
            if('↑' == arrow):
                self.shoot(x-1, y)
            elif('←' == arrow):
                self.shoot(x, y-1)
            elif('→' == arrow):
                self.shoot(x, y+1)
            elif('↓' == arrow):
                self.shoot(x+1, y)
            oldSquare.playerArrowDirection = ''


        newSquare = self.GameSquareMasterList[newX][newY]
        self.playerPos = (newX,newY)

        #Set the new player pos
        oldSquare.hasPlayer = False
        newSquare.hasPlayer = True

        newSquare.l.configure(background='white')

        if(oldSquare.getArrowDir()):
            newSquare.setArrowDir(oldSquare.getArrowDir())

        #Redraw
        oldSquare.reload()
        newSquare.reload()

        if('W' in newSquare.legend):
            tkMessageBox.showinfo(
                "LOST", 
                "You lost because you were eaten by the Wumpus\n"+
                "But, did the Wumpus win?"
            )
            exit()
        elif('P' in newSquare.legend):
            tkMessageBox.showinfo(
                "LOST", 
                "You fell into the pit D:"
            )
            exit()

    ###################################################
    # Constructor
    ###################################################
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
                playerArrowDirection=''
                if(item == 'S'):
                    hasPlayer = True
                    playerArrowDirection='↑'
                    self.playerPos = (x,y)
                elif(not item == 'E'):
                    itemLocations[item].append((x,y))

                gs = GameSquare(item, hasPlayer, playerArrowDirection)
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
    ###################################################
    # addWarnings
    ###################################################
    # Adds warnings to squares surrounding Pits, and 
    ###################################################
    # Params:
    # itemLocations - (x,y) pairs where items are located
    ###################################################
    def addWarnings(self, itemLocations):
        for item in itemLocations:

            for x,y in itemLocations[item]:
                warning = ''
                if('P' == item):
                    warning = 'Breeze'
                elif('W' == item):
                    warning = 'Smell'
              
                minX = x-1
                maxX = x+1
                minY = y-1
                maxY = y+1

                itemsToAddWarningTo = []

                if(minX >= 0):
                    itemsToAddWarningTo.append(self.GameSquareMasterList[minX][y])
                if(maxX < self.SIZE):
                    itemsToAddWarningTo.append(self.GameSquareMasterList[maxX][y])
                if(minY >= 0):
                    itemsToAddWarningTo.append(self.GameSquareMasterList[x][minY])
                if(maxY < self.SIZE):
                    itemsToAddWarningTo.append(self.GameSquareMasterList[x][maxY])

                for gbs in itemsToAddWarningTo:
                    if(str(item) not in gbs.legend and str(warning) not in gbs.legend): 
                        gbs.legend.append(warning)
                        gbs.reload()
    ###################################################
    # loop
    ###################################################
    # Runs the Tkinter loop thread
    ###################################################
    def loop(self):
        self.master.mainloop() 

###############################################################################
#MAIN
###############################################################################

fileLoc = sys.argv[1]
f = open(fileLoc, 'r')

file = f.read().strip().split("\n")

gb = GameBoard(list(file))

tkMessageBox.showinfo(
    "How To Play", 
    "Arrow keys to move.\n"+
    "Space to climb the ladder(|-|) or pick up the gold (☼).\n"+
    "Arrow direction (↑←↓→) can be controlled by ('w','a','s','d') respectfully. 'q' will fire"
)

gb.loop()
