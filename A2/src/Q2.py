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
StartDomain = 'January 17'
EndDomain = 'April 9'
Domains = []

#Using the text file supplied, we can touch the constraints
Constraints = fileLinesToArray('Assignment_Constraints.txt')

#For both the Domains and Constraints, go through and get the DoY rather than
#the text string.
Domains = range(
    dateStringToDayOfYear(StartDomain),
    dateStringToDayOfYear(EndDomain)+1
)

for i,Constraint in enumerate(Constraints):
    Constraints[i] = dateStringToDayOfYear(Constraint)

#midterm week
midtermDays = range(
    dateStringToDayOfYear('February 17'),
    dateStringToDayOfYear('February 24')+1 
)

#We cannot assign assignments during time so remove those values from the domain
Domains = list(set(Domains) - set(midtermDays))

#Print starting data
#print "Domains:",Domains
#print "ProhibitedConstraints:", midtermDays
#print "Constraints:",Constraints
#print
#print

bestDueDates = []
bestX = 0

#Loop through from 100 to 0
for N in range(5):
    prevAcceptableDomains = Domains[:]
    #Determine N
    for Domain in Domains:

        #Determine the range of freedom that is allowed
        minRange = Domain - N
        maxRange = Domain + N
        
        for Constraint in Constraints:
            #If the constraint is between the min and max range
            if(minRange <= Constraint and maxRange >= Constraint):
                #This number isnt acceptable
                Domains.remove(Domain)
                break

    #Determine X
    #If our list is in order, then the first and last items should be the min
    # and max due dates possible. We are just required to find 2 more based on
    # our X heuristic.
    for X in range(100):
        minDueDate = Domains[0]
        possibleDueDates = [minDueDate]

        recentDueDate = minDueDate

        for Domain in Domains:
            if(Domain == recentDueDate + X):
                recentDueDate = Domain
                possibleDueDates.append(Domain)
                if(len(possibleDueDates) == 4):
                    continue

        if(len(possibleDueDates) == 4 and X > bestX):
            possibleDueDatesStringArray = []
            for possibleDueDate in possibleDueDates:
                possibleDueDatesStringArray.append(dayOfYearToDateString(possibleDueDate))
            print "Found successful match for X:", X, "giving:", possibleDueDatesStringArray
            bestX = X
            bestDueDates = possibleDueDates[:]
        #else:
            #print "Did not find successful match", possibleDueDates
            
            



#If we still have Domains, print and continue
# if(Domains):
#     print "N:", N, "Domains:", Domains
# else:
#     print
#     print "The program tried to run N:",i,"but has finished with no successful results, here is the last successful results:"
#     for acceptedDomain in prevAcceptableDomains:
#         print acceptedDomain, "==", dayOfYearToDateString(acceptedDomain)
#     exit()
