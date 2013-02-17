###############################################################################
#Q1.py 
#CMPT 317 A2
#Quinn Neumiiller
#11065618
#qjn162
###############################################################################

#fileLinesToArray
#Splits a file up by new line and puts them in an array
#params: relativeFilePath - the relative file path to open
#returns: array - lines of the file without newline
def fileLinesToArray(relativeFilePath):
    f = open(relativeFilePath, 'r')
    returnArray = []
    for line in f:
        returnArray.append(line.strip())
    return returnArray

lines = fileLinesToArray('Midterm_Constraints.txt')

print lines