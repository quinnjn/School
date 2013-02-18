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
from time import strftime

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
#dateStringToDayOfYear
#------------------------------------------------------------------------------
#Given a date string (and possible a format) returns the day of year that
# date is
#params: datestring - string - some string representing a date
#optional params: format - string - The format to try parse the date string with
# default format is '%B %d' (Month day_of_month, ex March 11)
#returns: int - the day of year the dateString is
def dateStringToDayOfYear(dateString, format='%B %d'):
    date_struct = time.strptime(dateString, format)
    return date_struct[7]

#------------------------------------------------------------------------------
#dayOfYearToDateString
#------------------------------------------------------------------------------
#Given a day of year (and possible a format) returns the date string
#params: dayOfYear - int - number between 1 and 366 representing the day of year
#optional params: format - string - The format to try parse the date string with
# default format is '%B %d' (Month day_of_month, ex March 11)
#returns: string - the dateStirng the day of year is
def dayOfYearToDateString(dayOfYear, format='%B %d'):
    date_struct = time.strptime(str(dayOfYear), '%j')
    return strftime(format, date_struct)

#------------------------------------------------------------------------------
#main
#------------------------------------------------------------------------------

#These are the domains mentioned in the assignment
Domains = ['March 1', 'March 4', 'March 6', 'March 8', 'March 11', 'March 13', 'March 15']

#Using the text file supplied, we can touch the constraints
Constraints = fileLinesToArray('Midterm_Constraints.txt')

#For both the Domains and Constraints, go through and get the DoY rather than
#the text string.
for i,date in enumerate(Domains):
    Domains[i] = dateStringToDayOfYear(date)
print "Domains:", Domains

for i,Constraint in enumerate(Constraints):
    Constraints[i] = dateStringToDayOfYear(Constraint)
print "Constraints:",Constraints

#Loop through from 100 to 0
for i in range(100):
    prevAcceptableDomains = Domains[:]
    for Domain in Domains:

        #Determine the range of freedom that is allowed
        minRange = Domain - i
        maxRange = Domain + i
        
        for Constraint in Constraints:
            #If the constraint is between the min and max range
            if(minRange <= Constraint and maxRange >= Constraint):
                #This number isnt acceptable
                Domains.remove(Domain)
                break

    #If we still have Domains, print and continue
    if(Domains):
        print "N:", i, "Domains:", Domains
    else:
        print
        print "The program tried to run N:",i,"but has finished with no successful results, here is the last successful results:"
        for acceptedDomain in prevAcceptableDomains:
            print acceptedDomain, "==", dayOfYearToDateString(acceptedDomain)
        exit()

