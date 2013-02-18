###############################################################################
#Q1.py 
#CMPT 317 A2
#Quinn Neumiiller
#11065618
#qjn162
###############################################################################
#IMPORTS
###############################################################################
import time

###############################################################################
#FUNCTIONS
###############################################################################

#------------------------------------------------------------------------------
#fileLinesToArray
#------------------------------------------------------------------------------
#Splits a file up by new line and puts them in an array
#params: relativeFilePath - string - the relative file path to open
#returns: array - lines of the file without newline
def fileLinesToArray(relativeFilePath):
    f = open(relativeFilePath, 'r')
    returnArray = []
    for line in f:
        returnArray.append(line.strip())
    return returnArray

#------------------------------------------------------------------------------
#dateStringToDayOfYear
#------------------------------------------------------------------------------
#Given a date string (and possible a format) returns the day of year that
# date is
#params: datestring - string - some string representing a date
#optional params: format - string - The format to try parse the date string with
# default format is '%B %d'
#returns: int - the day of year the dateString is
def dateStringToDayOfYear(dateString, format='%B %d'):
    date_struct = time.strptime(dateString, format)
    return date_struct[7]



#------------------------------------------------------------------------------
#main
#------------------------------------------------------------------------------

Domains = ['March 1', 'March 4', 'March 6', 'March 8', 'March 11', 'March 13', 'March 15']
for i,date in enumerate(Domains):
    Domains[i] = dateStringToDayOfYear(date)
print Domains

Constraints = fileLinesToArray('Midterm_Constraints.txt')
for i,Constraint in enumerate(Constraints):
    Constraints[i] = dateStringToDayOfYear(Constraint)
print Constraints

for i in range(100,0, -1):
    for Domain in Domains:
        isAcceptable = True
        for Constraint in Constraints:
            if(Domain >= (Constraint+i) or Domain <= (Constraint-i)):
                isAcceptable = False
            #if(Domain > (Constraint+i) or Domain < (Constraint-i)):
                print Domain, Constraint, i
        if(isAcceptable):
            print Domain
            exit()
