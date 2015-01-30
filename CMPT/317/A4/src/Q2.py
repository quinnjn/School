###############################################################################
#Q2.py 
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
    # query
    #############################################
    def query(self,given):
        returnVar = ''
        p = None

        #Figure out the P(classVar) == true
        for cVarName, cVar in self.classVar.iteritems():
            p = cVar.P(True)

        #We have P(classVar), now multiply it by the sum of the evidence variables
        for eVarName, eVar in self.evidenceVar[True].iteritems():
            givenVal = given[eVarName]

            #Only compute 'Unobserved' values OR if the
            #user is observing T or F 
            if(givenVal == True or givenVal == False):# or givenVal == 'Unobserved'):
                print eVarName, eVar
                p = p * eVar.P(givenVal)
        return p
        
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
    print "Instructions"
    print "------------"
    print "To set enter \"<name>=true\", \"<name>=false\", or \"<name>=unobserved\""
    print "To query enter \"q\" or just <Enter>"
    print "To quit CTRL + Z or type \"quit\""

    #Start NBC, giving the text file locations.
    nbc = NBC(sys.argv[1], sys.argv[2])
    print "\nCurrent data:"
    print nbc

    #Set user defined evidense bars
    evidenceVarNames = {}
    for key in nbc.evidenceVar[True].keys():
        evidenceVarNames[key] = 'Unobserved'

    print "User defined evidece variable status:"
    print evidenceVarNames
    print "\n"

    #Build the regex
    query = re.compile('([A-Z]+)(\s*=\s*(TRUE|FALSE|UNOBSERVED))*', re.IGNORECASE)

    while(True):
        rawinput = raw_input('?- ')
        input = rawinput.upper()
        m = query.search(input)

        if('Q' == input or '' == input):
            print 'Querying!'
            print nbc.query(evidenceVarNames)
        elif('QUIT' == input):
            exit()
        elif(m.group(3)):
            name = m.group(1)
            val  = m.group(3)

            found = False
            for eVarName in evidenceVarNames.keys():
                if(name.upper() == eVarName.upper()):
                    found = True
                    if('TRUE' == val):
                        val = True
                    elif('FALSE' == val):
                        val = False
                    else:
                        val = val.title()

                    evidenceVarNames[eVarName] = val
                    print evidenceVarNames
            if(not found):
                print name,"isnt a evidence variable"
        else:
            print "I dont understand:", rawinput


if(__name__ == '__main__'):
    main()
