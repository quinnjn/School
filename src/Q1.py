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

    def getVal(self, value):
        if(value):
            return self.true
        else:
            return self.false

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

    #############################################
    # toString
    #############################################
    def __str__(self):
        returnString = "\n"
        returnString += 'Evidence Variables:\n'
        for key, val in self.evidenceVar.iteritems():
            for bool in [True,False]:
                returnString += "\tP(%s == %r) \t= %d/%d or %0.2f\n" % (key, bool, val.getVal(bool), val.total(), val.P(bool))

        returnString += '\nClass Variables\n'
        for key, val in self.classVar.iteritems():
            for bool in [True,False]:
                returnString += "\tP(%s == %r) \t= %d/%d or %0.2f\n" % (key, bool, val.getVal(bool), val.total(), val.P(bool))

        return returnString
    
    #############################################
    # Constructor
    #############################################
    def __init__(self, fileWithStructure, fileWithData):
        self.loadStructure(fileWithStructure)
        self.loadData(fileWithData)

    #############################################
    # loadData
    #############################################
    # Loads the data of the NBC
    #############################################
    # Params:
    # file : string - the string of the file
    #   we are loading
    #############################################
    def loadData(self, file):
        f = open(file, 'r')
        f = f.read().split('\n')
        for line in f:
            #If it's a blank line, skip it
            if(not line):
                continue
            line = line.split('\t')
            for assignment in line:
                #Do some regex on the line to grab the true or false
                #along with the variable name.
                m = re.search('(.*?):(TRUE|FALSE)', assignment)

                name = m.group(1)
                val = m.group(2)

                #If it's true, set it as true. False otherwise
                val = (val.upper() == 'TRUE')

                if(name in self.classVar):
                    self.classVar[name].observe(val)
                elif(name in self.evidenceVar):
                    self.evidenceVar[name].observe(val)

    #############################################
    # loadStructure
    #############################################
    # Loads the structure of the NBC
    #############################################
    # Params:
    # file : string - the string of the file
    #   we are loading
    #############################################
    def loadStructure(self, file):
        classVar = {}
        evidenceVar = {}

        f = open(file, 'r')
        f = f.read().split('\n')

        for line in f:
            #If it's a blank line, skip it
            if(not line):
                continue
            if(not classVar):
                classVar[line] = NBCVariable()
            else:
                evidenceVar[line] = NBCVariable()

        #Set the vars as class variables
        self.classVar    = classVar
        self.evidenceVar = evidenceVar
    

#############################################
# MAIN
#############################################
def main():
    #Start NBC, giving the text file locations.
    nbc = NBC(sys.argv[1], sys.argv[2])
    print nbc


if(__name__ == '__main__'):
    main()
