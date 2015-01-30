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
        # print "PRESSING", doing
        self.gb.keyPress(doing)

    ###################################################
    # clean
    ###################################################
    # Clean up any extra stuff that looms in our KB
    # that may not be valid anymore
    ###################################################
    def clean(self):
        for pos in self.Safe:
            if pos in self.PossibleWumpusLocs:
                self.PossibleWumpusLocs.remove(pos)
            elif pos in self.PossiblePitLocs:
                self.PossiblePitLocs.remove(pos)
        
        # print "Current", self.loc
        # print "PWL", self.PossibleWumpusLocs
        # print "PPL", self.PossiblePitLocs
        # print "SAFE", self.Safe
        # print "UNV", self.Unvisited
        # print

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
        
        #aim
        if(x > aimX):
            self.move('w')
        elif(x < aimX):
            self.move('s')
        elif(y > aimY):
            self.move('a')
        elif(y < aimY):
            self.move('d')

        #fire
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
            #For each legend location, try deduce where things are
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

    #!!!
    #NOT FINISHED
    #I intended to do some path planning, but due to time I just let him randomly walk around.
    #!!!

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

        #Figure out which range we can navigate too.
        ranges = [
            (x-1,y),
            (x+1,y),
            (x,y-1),
            (x,y+1)
        ]

        #Loop through and remove unvalid locations
        for rX, rY in ranges[:]:
            if(toPos == (rX,rY)):
                return pathSoFar
            elif(not self.validRange(rX,rY) or (rX,rY) not in self.Safe):
                ranges.remove((rX,rY))

        #Loop through the ranges 
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
        #Figure out which range we can navigate too.
        ranges = [
            (x-1,y),
            (x+1,y),
            (x,y-1),
            (x,y+1)
        ]
        #Find any unvalid ranges
        for x,y in ranges[:]:
            if(not self.validRange(x,y) or (x,y) in self.PossiblePitLocs or (x,y) in self.PossibleWumpusLocs):# or (x,y) in self.Safe):
                print (x,y),"remove"
                ranges.remove((x,y))
            else:
                print (x,y),"keep"

        #Random choice of choices we can goto.
        x,y = choice(ranges)

        #Pick a location to move.
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
        #Default color is black to hide the square.
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
        #Join the legend together to print.
        returnString = ', '.join(self.legend)
        #Replace gold with ☼ character
        returnString = returnString.replace('G', '☼')
        #Print the ASCII player
        if(self.hasPlayer):
            returnString +=  "\n"
            returnString += "o\n"
            returnString += "/|\\"
            returnString += self.playerArrowDirection
            returnString += "\n"
            returnString += "/ \\\n"
        #Print the ASCII ladder
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
# The GameBoard object
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
        #Grab the wumpus square.
        oldSquare = self.GameSquareMasterList[x][y]

        #If we actually shot at the wumpus, kill him
        if('W' in oldSquare.legend):
            oldSquare.legend.remove('W')

            minX = x-1
            maxX = x+1
            minY = y-1
            maxY = y+1

            #If we killed the wumpus, purge the smell
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
    def keyPress(self,event):
        print "not here"
        self.keyPress(event.keysym)
    ###################################################
    # keyPress
    ###################################################
    # Accepts a key as input and updates the game board
    # depending on the action recieved
    ###################################################
    # Params:
    # key - What the autonomous agent would press
    ###################################################
    def keyPress(self, key):
        print "GB PRESSED", key
        #key = event.keysym
        x,y = self.playerPos
        newX,newY = x,y

        oldSquare = self.GameSquareMasterList[x][y]
        #up arrow key, go up.
        if("Up" == key):
            #If we hit the top, dont keep going.
            if(x == 0):
                return
            newX -= 1
        #down arrow key, go down
        elif("Down" == key):
            #If we are at SIZE, dont keep going.
            if(x == self.SIZE-1):
                return
            newX += 1
        #left arrow key, left
        elif("Left" == key):
            #If we hit the left most side, dont keep going
            if(y == 0):
                return
            newY -= 1
        #Right arrow key, go right
        elif("Right" == key):
            #If we hit the right most side, dont keep going
            if(y == self.SIZE-1):
                return
            newY += 1
        #space, action key
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
        #w, arrow direction up
        elif("w" == key and oldSquare.playerArrowDirection):
            oldSquare.playerArrowDirection = '↑'
        #a, arrow direction left
        elif("a" == key and oldSquare.playerArrowDirection):
            oldSquare.playerArrowDirection = '←'
        #d, arrow direction right
        elif("d" == key and oldSquare.playerArrowDirection):
            oldSquare.playerArrowDirection = '→'
        #s, arrow direction down
        elif("s" == key and oldSquare.playerArrowDirection):
            oldSquare.playerArrowDirection = '↓'
        #q, shoot the arrow
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

        #MAke sure the square is now visible after stepping on it.
        newSquare.l.configure(background='white')
        newSquare.backgroundColor='white'

        #Set the new arrow direction from the old oen.
        if(oldSquare.getArrowDir()):
            newSquare.setArrowDir(oldSquare.getArrowDir())

        #Redraw
        oldSquare.reload()
        newSquare.reload()

        #If the legend has a wumpus, the player has stepped on the wumpus and failed.
        if('W' in newSquare.legend):
            tkMessageBox.showinfo(
                "LOST", 
                "You lost because you were eaten by the Wumpus\n"+
                "But, did the Wumpus win?"
            )
            exit()

        #If the legend has a pit, the player has stepped in the pit and failed.
        elif('P' in newSquare.legend):
            tkMessageBox.showinfo(
                "LOST", 
                "You fell into the pit D:"
            )
            exit()

    ###################################################
    # giveInfoToAgent
    ###################################################
    # Passes along information the agent needs to know about
    # but nothing more
    ###################################################
    def giveInfoToAgent(self):
         #Make sure we give info to the Agent again, after 0.5 seconds.
         self.master.after(500, self.giveInfoToAgent)
         x,y = self.playerPos
         legend = self.GameSquareMasterList[x][y].legend

         hasArrow = False
         arrow = self.GameSquareMasterList[x][y].getArrowDir()
         #IF the arrow is available, tell its direction 
         if(arrow):
            if('↑' == arrow):
                hasArrow = 'Up'
            elif('←' == arrow):
                hasArrow = 'Left'
            elif('→' == arrow):
                hasArrow = 'Right'
            elif('↓' == arrow):
                hasArrow = 'Down'

         #Give the agent the current location, legend on the current location
         # and if the arrow exists, which direction
         self.agent.tell({
            'currentLocation':self.playerPos,
            'legend':legend,
            'hasArrow':hasArrow
         })

    ###################################################
    # Constructor
    ###################################################
    # Params:
    # textBoard - The board in text format to be generated
    # agent - the reference to the agent to send info to
    ###################################################
    def __init__(self, textBoard, agent):
        self.agent = agent
        self.playerPos = None
        master = Tk()

        #master.bind("<Key>", self.keyPress)
        master.title("Wumpus' Dungeon")
        self.SIZE = int(textBoard.pop(0))

        #Item locations dictionary
        itemLocations = {
            'G':[],
            'P':[],
            'W':[]
        }

        #loop through X and Y coords and build the GameSquares
        GameSquareMasterList = list()
        for x in range(self.SIZE):

            GameSquareList = list()
            for y in range(self.SIZE):

                item = textBoard[x][y]

                hasPlayer = False
                playerArrowDirection=''

                #Is it a starting location?
                if(item == 'S'):
                    hasPlayer = True
                    #Add the ArrowDirection and use this as the player position.
                    playerArrowDirection='↑'
                    self.playerPos = (x,y)
                #If the item is not Empty, append it to the itemLocations.
                elif(not item == 'E'):
                    itemLocations[item].append((x,y))

                #Create the GameSquare
                gs = GameSquare(item, hasPlayer, playerArrowDirection)

                #Add the GameSquare to the list.
                GameSquareList.append(gs)

                #Create the label for the GameSquare
                gs.label(
                    master
                ).grid(
                    row=x, 
                    column=y
                )       

            #Add this y list to the master list
            GameSquareMasterList.append(GameSquareList)

        #Set globals for the class.
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

            #Go through itemlocations and add their warnings.
            for x,y in itemLocations[item]:
                warning = ''
                if('P' == item):
                    warning = 'Breeze'
                elif('W' == item):
                    warning = 'Smell'
                else:
                    continue

                #Figure out the min/max for X/Y
                minX = x-1
                maxX = x+1
                minY = y-1
                maxY = y+1

                itemsToAddWarningTo = []

                #Append warnings to their GameSquare List.
                if(minX >= 0):
                    itemsToAddWarningTo.append(self.GameSquareMasterList[minX][y])
                if(maxX < self.SIZE):
                    itemsToAddWarningTo.append(self.GameSquareMasterList[maxX][y])
                if(minY >= 0):
                    itemsToAddWarningTo.append(self.GameSquareMasterList[x][minY])
                if(maxY < self.SIZE):
                    itemsToAddWarningTo.append(self.GameSquareMasterList[x][maxY])

                #For each of the items to add warnings to, make sure we should add the warning.
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
        #Tell the agent after a second about the Gameboard, this is to avoid nulls
        self.master.after(1000, self.giveInfoToAgent)
        #Run mainloop
        self.master.mainloop()


###############################################################################
#MAIN
###############################################################################

#Get the file location from file and open it.
fileLoc = sys.argv[1]
f = open(fileLoc, 'r')

#Read the file, strip the file, and split the file by newline.
file = f.read().strip().split("\n")

#Get the size to tell the AutonomousAgent
SIZE = int(file[0])

#Create a new AutonomousAgent
agent = AutonomousAgent(SIZE)

#Create a new Gameboard with the file and agent
gb = GameBoard(list(file), agent)

#Tell the agent what the gameboard is to send keys to it.
agent.setGameBoard(gb)

#Run the loop
gb.loop()
