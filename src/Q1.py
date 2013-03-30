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
    # getObservedValue
    #############################################
    # Returns the observed value
    #############################################
    # Params:
    # value : boolean - which observed value
    #   you want to view
    #############################################
    # Returns:
    # Boolean - the observed value specified.
    #############################################
    def getObservedValue(self, value):
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
        returnString = ""

        #The things we want to print
        toPrint = {
            'Class Variables'   :self.classVar,
            'Class(True) Evidence Variables':self.evidenceVar[True],
            'Class(False) Evidence Variables':self.evidenceVar[False]
        }

        #loop through the variable name and lists
        for varName, varList in sorted(toPrint.items()):
            returnString += '\n'+varName+':\n'
            #For each list, iterate through the variables
            for key, val in varList.iteritems():
                #We want to check values for True and False so loop through both.
                for bool in [True,False]:
                    returnString += "\tP(%s == %r) \t= %d/%d or %0.2f\n" % (key, bool, val.getObservedValue(bool), val.total(), val.P(bool))

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

        currentClassVarValue = None

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
                    currentClassVarValue = val
                elif(name in self.evidenceVar[True]):
                    self.evidenceVar[currentClassVarValue][name].observe(val)


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
        evidenceVar = {
            True:{},
            False:{}
        }

        f = open(file, 'r')
        f = f.read().split('\n')

        for line in f:
            #If it's a blank line, skip it
            if(not line):
                continue
            if(not classVar):
                classVar[line] = NBCVariable()
            else:
                evidenceVar[True][line] = NBCVariable()
                evidenceVar[False][line] = NBCVariable()

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
