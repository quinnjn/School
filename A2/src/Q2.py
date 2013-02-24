###############################################################################
#Q2.py 
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
    dateStringToDayOfYear(EndDomain)+1 #Including this date, range in python is exclusive
)

for i,Constraint in enumerate(Constraints):
    Constraints[i] = dateStringToDayOfYear(Constraint)

#midterm week
midtermDays = range(
    dateStringToDayOfYear('February 17'),
    dateStringToDayOfYear('February 24')+1 #Including this date, range in python is exclusive
)

#We cannot assign assignments during time so remove those values from the domain
Domains = list(set(Domains) - set(midtermDays))


#This will be the domains without constraints
#We are defining this out of the loop because as N increases we just remove
#more items.
DomainsWithoutConstraints = Domains[:]

#Loop through from 100 to 0
for N in range(5):
    print "--- N = %d ---" % N

    #This is a temp list that we loop over, removing items from DomainsWithoutConstraints
    tempDomains = DomainsWithoutConstraints[:]

    #Determine N
    #This can be optimized by just reusing DomainsWithoutConstraints
    for Domain in tempDomains:

        #Determine the range of freedom that is allowed
        minRange = Domain - N
        maxRange = Domain + N
        
        #Loop through the constraints and remove items that shouldn't be there
        for Constraint in Constraints:
            #If the constraint is between the min and max range
            if(minRange < Constraint and Constraint < maxRange):
                #This number isnt acceptable with our constraints, removing it
                DomainsWithoutConstraints.remove(Domain)
                #We can break at this point because we cant re-remove the item
                break


    #At this point, DomainsWithoutConstraints includes the dates that are acceptable given our Constraint
    #So any of these due dates will not interfere with our constraints

    #Determine X
    #If our list is in order (which it is), then the first and last items should be the min
    # and max due dates possible. We are just required to find 2 more based on
    # our X heuristic.
    print "Removed %d problematic domains from the original %d" %((len(Domains) - len(DomainsWithoutConstraints)), len(Domains))

    #Loop through some range of X, in this case 1-100
    for X in range(100+1): #Including this date, range in python is exclusive
        minDueDate = DomainsWithoutConstraints[0]
        possibleDueDates = [minDueDate]
        recentDueDate = minDueDate

        checkedDomains = 0
        #loop through the DomainsWithoutConstraints trying to find acceptable dates
        for Domain in DomainsWithoutConstraints:
            checkedDomains += 1
            #If the domain is greater than or equal to the last assignment date + X, we can use this number.
            if(Domain >= recentDueDate + X):
                recentDueDate = Domain
                possibleDueDates.append(Domain)

                #If we hit 4 dates its good to go
                if(len(possibleDueDates) == 4):
                    continue

        if(len(possibleDueDates) == 4):
            possibleDueDatesStringArray = []
            #This is cleaning up from DoY to a string that is easy to read.
            for possibleDueDate in possibleDueDates:
                possibleDueDatesStringArray.append(dayOfYearToDateString(possibleDueDate))
            print "N:", N, "X:", X, "nodes checked:",checkedDomains,"giving:", possibleDueDatesStringArray
    print          
