# -*- coding: utf-8 -*- 
###############################################################################
#Q2.py 
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

from copy import deepcopy
from random import choice

from time import sleep
        
###############################################################################
#CLASS
###############################################################################

###################################################
# AutonmousAgent
###################################################
# Our Wumpus world navigating robot
###################################################
class AutonomousAgent():

    ###################################################
    # constructor
    ###################################################
    def __init__(self, size):
        self.FoundGold = False
        self.Unvisited = []
        for x in range(SIZE):
            for y in range(SIZE):
                self.Unvisited.append((x,y))

        self.SIZE = size
        self.Safe = []
        self.PossibleWumpusLocs = []
        self.PossiblePitLocs = []
        self.toMoveList = []

    ###################################################
    # validRange
    ###################################################
    # Determines if a x,y pair is actually valid
    ###################################################
    # Params:
    # x - X coord
    # y - Y coord
    ###################################################
    # Returns:
    # boolean - True if the valid range is accepted
    #   otherwise false
    ###################################################
    def validRange(self,x,y):
        return ((x>=0 and x<self.SIZE)and(y>=0 and y<self.SIZE))

    ###################################################
    # setGameBoard
    ###################################################
    # Let's the AutonmousAgent know about the gameboard
    # This is to send key presses into the gameboard
    ###################################################
    # Params:
    # gb - The GameBoard instance
    ###################################################
    def setGameBoard(self, gb):
        self.gb = gb

    ###################################################
    # move
    ###################################################
    # Tells the gameboard the direction the 
    # AutonmousAgent thinks to go
    ###################################################
    # Params:
    # doing - What the AutonomousAgent wants to do
    ###################################################
    def move(self, doing):
        print "PRESSING", doing
        self.gb.keyPress(doing)

    ###################################################
    # clean
    ###################################################
    # Clean up any extra stuff that looms in our KB
    ###################################################
    def clean(self):
        for pos in self.Safe:
            if pos in self.PossibleWumpusLocs:
                self.PossibleWumpusLocs.remove(pos)
            elif pos in self.PossiblePitLocs:
                self.PossiblePitLocs.remove(pos)
        
        print "Current", self.loc
        print "PWL", self.PossibleWumpusLocs
        print "PPL", self.PossiblePitLocs
        print "SAFE", self.Safe
        print "UNV", self.Unvisited
        print

    ###################################################
    # dedeuceLocations
    ###################################################
    # Params:
    # list - The list we want to add possible locations to
    ###################################################
    def deduceLocations(self,list):
        x,y = self.loc
        ranges = [
            (x-1,y),
            (x+1,y),
            (x,y-1),
            (x,y+1)
        ]

        for x,y in ranges:
            if(self.validRange(x,y) and (x,y) not in list):# or (x,y) in self.Safe):
                list.append((x,y))

    ###################################################
    # shoot
    ###################################################
    # The AutonomousAgent determines an attack
    ###################################################
    def shoot(self):
        toAim = choice(self.PossibleWumpusLocs)
        self.PossibleWumpusLocs.remove(toAim)

        x,y = self.loc
        aimX,aimY = toAim

        print "FIRE", self.loc, toAim

        if(x > aimX):
            self.move('w')
        elif(x < aimX):
            self.move('s')
        elif(y > aimY):
            self.move('a')
        elif(y < aimY):
            self.move('d')

        self.move('q')




    ###################################################
    # tell
    ###################################################
    # The Gameboard 'tells' the AutonomousAgent 
    # where to go. 
    ###################################################
    # Params:
    # info - Information from our GameBoard
    ###################################################
    def tell(self, info):
        if(self.FoundGold):
            exit()

        print info
        self.loc = info['currentLocation']
        self.arrow = info['hasArrow']
        if(self.loc not in self.Safe):
            self.Safe.append(self.loc)
            self.Unvisited.remove(self.loc)

        if(self.toMoveList):
            move(self.toMoveList.pop(0))
        # elif(len(self.Safe) == 1):
        #     #We have no data from the gameboard
        #     #Take a random step.
        #     self.move(self.randomWalk())
        else:
            for legend in info['legend']:
                if('Smell' == legend):
                    self.deduceLocations(self.PossibleWumpusLocs)
                    self.shoot()

                elif('Breeze' == legend):
                    self.deduceLocations(self.PossiblePitLocs)
                    print 'here'
                elif('W' == legend or 'P' == legend):
                    exit(-1)
                elif('G' == legend and not self.FoundGold):
                    self.FoundGold = True
                    self.move('space')
                    exit()

        
        #self.findPath((3,1),(2,0))
        self.clean()
        self.move(self.randomWalk())
        print "====="

    ###################################################
    #FindPath
    ###################################################
    # Finds a path from one position to another
    ###################################################
    # Params:
    # fromPos the (x,y) pair with the starting position
    # toPos the (x,y) pair we are finding a path to
    # pathSoFar the recursive path that we have so far
    ###################################################
    # Returns:
    # list of (x,y) pairs showing the safest path
    ###################################################
    def findPath(self, fromPos, toPos, pathSoFar = []):
        x, y = fromPos

        ranges = [
            (x-1,y),
            (x+1,y),
            (x,y-1),
            (x,y+1)
        ]

        for rX, rY in ranges[:]:
            if(toPos == (rX,rY)):
                return pathSoFar
            elif(not self.validRange(rX,rY) or (rX,rY) not in self.Safe):
                ranges.remove((rX,rY))

        for pos in ranges:
            temp = pathSoFar[:]
            temp.append(pos)
            pathSoFar = self.findPath(pos, toPos, temp)


    ###################################################
    # randomWalk
    ###################################################
    # Returns some hopefully safe direction to move.
    ###################################################
    def randomWalk(self):
        returnMove = ''
        origX,origY = self.loc
        x,y = origX,origY
        ranges = [
            (x-1,y),
            (x+1,y),
            (x,y-1),
            (x,y+1)
        ]
        print ranges
        for x,y in ranges[:]:
            if(not self.validRange(x,y) or (x,y) in self.PossiblePitLocs or (x,y) in self.PossibleWumpusLocs):# or (x,y) in self.Safe):
                print (x,y),"remove"
                ranges.remove((x,y))
            else:
                print (x,y),"keep"

        x,y = choice(ranges)

        print self.loc, (x,y)

        if(x > origX):
            returnMove = 'Down'
        elif(x < origX):
            returnMove = 'Up'
        elif(y > origY):
            returnMove = 'Right'
        elif(y < origY):
            returnMove = 'Left'
        print "moving to:", returnMove
        return returnMove

###############################################################################
#CLASS
###############################################################################

###############################################################################
#GameSquare
###############################################################################
# The GameSquare object
###############################################################################
class GameSquare:
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

    def label(self, master):
        self.l = Label(
            master,
            textvariable = self.string,
            background = self.backgroundColor,
            width = 15,
            height = 5
        )
        return self.l

    def getArrowDir(self):
        return self.playerArrowDirection
    def setArrowDir(self, arrowDir):
        self.playerArrowDirection = arrowDir


    def reload(self):
        self.string.set(self)
        
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
    def validRange(self,x,y):
        return ((x>=0 and x<self.SIZE)and(y>=0 and y<self.SIZE))
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

    def keyPress(self,event):
        print "not here"
        self.keyPress(event.keysym)

    def keyPress(self, key):
        print "GB PRESSED", key
        #key = event.keysym
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
        newSquare.backgroundColor='white'

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

        
    def giveInfoToAgent(self):
         self.master.after(500, self.giveInfoToAgent)
         x,y = self.playerPos
         legend = self.GameSquareMasterList[x][y].legend

         hasArrow = False
         arrow = self.GameSquareMasterList[x][y].getArrowDir()
         if(arrow):
            if('↑' == arrow):
                hasArrow = 'Up'
            elif('←' == arrow):
                hasArrow = 'Left'
            elif('→' == arrow):
                hasArrow = 'Right'
            elif('↓' == arrow):
                hasArrow = 'Down'


         self.agent.tell({
            'currentLocation':self.playerPos,
            'legend':legend,
            'hasArrow':hasArrow
         })


        #  G = []
        #  S = None
        #  Smells = []
        #  Breeze = []

        #  for x in range(self.SIZE):
        #     for y in range(self.SIZE):
        #         currentSquare = self.GameSquareMasterList[x][y]

        #         if(currentSquare.backgroundColor == 'black'):
        #             continue
        #         else:
        #             print x,y

        #         for label in currentSquare.legend:
        #             if('Smell' == label):
        #                 Smells.append((x,y))
        #             elif('Breeze' == label):
        #                 Breeze.append((x,y))


        #  self.agent.tell({
        #     'G': G,
        #     'Start': S,
        #     'Smells': Smells,
        #     'Breeze' : Breeze,
        #     'ArrowDirection': None,
        #     'currentLocation': self.playerPos
        # })

    def __init__(self, textBoard, agent):
        self.agent = agent
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

    def addWarnings(self, itemLocations):
        for item in itemLocations:

            for x,y in itemLocations[item]:
                warning = ''
                if('P' == item):
                    warning = 'Breeze'
                elif('W' == item):
                    warning = 'Smell'
                #elif('G' == item):
                #    print 'G'
                else:
                    continue

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

    def loop(self):
        self.master.after(1000, self.giveInfoToAgent)
        self.master.mainloop()


###############################################################################
#FUNCTIONS
###############################################################################

fileLoc = sys.argv[1]
f = open(fileLoc, 'r')

file = f.read().strip().split("\n")

SIZE = int(file[0])

agent = AutonomousAgent(SIZE)

gb = GameBoard(list(file), agent)

agent.setGameBoard(gb)


# tkMessageBox.showinfo(
#     "How To Play", 
#     "Arrow keys to move.\n"+
#     "Space to climb the ladder(|-|) or pick up the gold (☼).\n"+
#     "Arrow direction (↑←↓→) can be controlled by ('w','a','s','d') respectfully. 'q' will fire"
#)

gb.loop()
