###############################################################################
#Q1.py 
#CMPT 317 A4
#Quinn Neumiiller
#11065618
#qjn162
###############################################################################
#IMPORTS
###############################################################################
import sys
import re

###############################################################################
#CLASS
###############################################################################

#############################################
# NBCVariable
#############################################
# Class representing the NBCVariable, holding
# any data for the NBCVariable
#############################################
class NBCVariable:
    #############################################
    # constructor
    #############################################
    def __init__(self):
        self.true = 0
        self.false = 0

    #############################################
    # P
    #############################################
    # Returns the probability that this 
    # variable is (either T/F).
    #############################################
    # Params:
    # value : boolean - T/F depending on what 
    #   value we want to see the probability for
    #############################################
    def P(self, value):
        returnVal = 0.0
        total = self.total()

        if(value):
            value = self.true
        else:
            value = self.false
        # the total is always greater than true
        # or false
        # so we dont need to actually check
        # if the total is not equal to 0.
        if(value != 0):
            returnVal = float(float(value) / float(self.total()))
        return returnVal
    #############################################
    # total
    #############################################
    # Returns the total values recorded
    # for this variable.
    #############################################
    def total(self):
        return float(self.true) + float(self.false)

    #############################################
    # observe
    #############################################
    # Params:
    # value : boolean - True if the the observation
    #   is true, false otherwise.
    #############################################
    # Increments the observed variable 
    #############################################
    def observe(self, value):
        if(value):
            self.true += 1
        else:
            self.false += 1

    #############################################
    # __repr__
    #############################################
    # Special toString that is called when
    # the dictionary is being printed.
    # We dont need anything special, so just
    # rely on what the toString says
    #############################################
    def __repr__(self):
        return self.__str__()
    #############################################
    # __str__ (toString)
    #############################################
    def __str__(self):
        total = self.total()
        returnString  = "T(%d/%d == %0.2f)" % (self.true,  total, self.P(True) )
        returnString += " "
        returnString += "F(%d/%d == %0.2f)" % (self.false, total, self.P(False))
        return returnString

#############################################
# NBC
#############################################
# The Naive Bayesian Classifier
#############################################
class NBC:

    def __init__(self, fileWithStructure, fileWithData):
        self.loadStructure(fileWithStructure)
        self.loadData(fileWithData)

    def loadData(self, file):
        f = open(file, 'r')
        f = f.read().split('\n')
        for line in f:
            if(not line):
                continue
            line = line.split('\t')
            for assignment in line:

                m = re.search('(.*?):(TRUE|FALSE)', assignment)

                name = m.group(1)
                val = m.group(2)

                if(val.upper() == 'TRUE'):
                    val = True
                else:
                    val = False

                if(name in self.classVar):
                    self.classVar[name].observe(val)
                elif(name in self.evidenceVar):
                    self.evidenceVar[name].observe(val)


        print self.evidenceVar

    def loadStructure(self, file):
        classVar = {}
        evidenceVar = {}

        f = open(file, 'r')
        f = f.read().split('\n')

        for line in f:
            if(not line):
                continue
            if(not classVar):
                classVar[line] = NBCVariable()
            else:
                evidenceVar[line] = NBCVariable()

        self.classVar    = classVar
        self.evidenceVar = evidenceVar
    

NBC(sys.argv[1], sys.argv[2])