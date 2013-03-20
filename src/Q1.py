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
    # propability
    #############################################
    # Returns the probability that this 
    # variable is true.
    #############################################
    def propability(self):
        returnVal = 0.0
        total = self.total()
        # the total is always greater than true
        # so we dont need to actually check
        # if the total is not equal to 0.
        if(self.true != 0):
            returnVal = float(float(self.true) / float(self.total()))
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
        return "%d/%d == %0.2f" % (self.true, self.total(), self.propability())

#############################################
# NBC
#############################################
# The Naive Bayesian Classifier
#############################################
class NBC:
    
    def __init__(self, fileWithStructure, fileWithData):
        self.loadStructure(fileWithStructure)
        self.loadData(fileWithData)

    def loadData(self, fileWithData):
        f = open(fileWithData, 'r')
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

    def loadStructure(self, fileWithStructure):
        classVar = {}
        evidenceVar = {}

        f = open(fileWithStructure, 'r')
        f = f.read().split('\n')

        for line in f:
            if(not line):
                continue
            if(not classVar):
                classVar[line] = NBCVariable(line)
            else:
                evidenceVar[line] = NBCVariable(line)

        self.classVar    = classVar
        self.evidenceVar = evidenceVar
    

NBC(sys.argv[1], sys.argv[2])