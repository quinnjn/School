###############################################################################
#Q3P2.py 
#CMPT 317 A2
#Quinn Neumiiller
#11065618
#qjn162
###############################################################################
###############################################################################
#IMPORTS
###############################################################################
import signal
from time import sleep, clock

###############################################################################
#GLOBALS
###############################################################################
NODES_SEARCHED = 0

###############################################################################
#FUNCTIONS
###############################################################################
def BacktrackSearch(csp):
    return Backtrack({}, csp)

#  function BacktrackingSearch(csp) returns a solution, or failure
#   return Backtrack({}, csp)
#
#  function Backtracking-Search(assignment, csp) returns a solution, or failure
def Backtrack(assignment, csp):
    global NODES_SEARCHED
    #Pulling out references to each part of the CSP
    Variables = csp['Variables']
    Domains = csp['Domains']
    VariableDomains = csp['VariableDomains']
    Constraints = csp['Constraints']

    #   if assignment is complete then return assignment
    #My reasoning of this is if Variables is empty, return.
    if(not Variables):
        return assignment
    #   var <- Select-Unassigned-Variable(csp)
    #First unassigned Variable
    var = Variables.pop(0)
    #   for each value in Order-Domain-Values(var, assignment, csp) do
    for value in Domains:
        NODES_SEARCHED+= 1
        #   if value is consistent with assignment then
        #Check if this monster can reside in a bungalow here
        #If this place is not listed as a place the monster can reside
        #continue.
        if(value not in VariableDomains[var]):
            continue
        #The monster agrees this place looks like a good place to raise the little monsters
        #Next, we need to make sure that our enemy is here or not here depending on the constraint.
        passesConstraint = True
        for constraint in Constraints:
            compariableMonster = constraint[2]
            #If there is a constraint for this monster
            if(constraint[0] == var):
                #passesConstraint = False
                #If we are looking for a compariableMonster and he doesnt have a place yet, or this isnt the place try another.
                if(constraint[1] == '==' and (compariableMonster not in assignment or assignment[compariableMonster] != value)):
                    passesConstraint = True
                #If we are avoiding a monster, check if he has a place and his place is our prospective one.
                elif(constraint[1] == '!='and compariableMonster in assignment and assignment[compariableMonster] == value):
                    passesConstraint = False
                break

        if(passesConstraint):
        #   add{var = value} to assignment
            assignment[var] = value
            result = Backtrack(assignment, csp)
            if(result):
                return result
            else:
                del assignment[var]

    #if assignment[var] is not set, readd it.
    if(var not in assignment):
        Variables.append(var)
    return False

    #   inferences <- Inference(csp, var, value)
    #   if inferences != failure then
    #   add inferences to assignment
    #   result <- Backtrack(assignment, csp)
    #   if result != faulure then
    #   return result
    #   remove {var = value} and inferences from assignment
    #   return failure
    #global Variables

        #If still unassigned, append.
        #Variables.append(var)

###############################################################################
#MAIN
###############################################################################

#Our CSP
csp = {
    #All the variables
    #V = {G, M, R, MG, K}
    'Variables':[
        "Godzilla", 
        "Mothra", 
        "Rodan", 
        "MechaGodzilla", 
        "King Kong"
    ],
    #All the domains
    #D = {P, N, B, T}
    'Domains':[
        "Paris",
        "New York",
        "Beijing",
        "Tokyo"
    ],
    #The acceptable domains for each variable
    'VariableDomains':{
        #D_G = {N, T}
        'Godzilla':[
            'Tokyo',
            'New York'
        ],
        #D_M = {P, N, B, T}
        'Mothra':[
            "Paris",
            "New York",
            "Beijing",
            "Tokyo"
        ],
        #D_K = {N, P}
        'King Kong':[
            'New York',
            'Paris'
        ],
        #D_{MG} = {P, N, B}
        'MechaGodzilla':[
            'Paris',
            'New York',
            'Beijing'
        ],
        #D_R = {P, N, B, T}
        'Rodan':[
            "Paris",
            "New York",
            "Beijing",
            "Tokyo"
        ]
    },
    #All the constraints
    #C={M != R, R != M, K != G, G != K, MG==G or MG==M}
    'Constraints':[[
        'Mothra',
        '!=',
        'Rodan'
    ],[
        'Rodan',
        '!=',
        'Mothra'
    ],[
        'Godzilla',
        '!=',
        'King Kong'
    ],[
        'King Kong',
        '!=',
        'Godzilla'
    ],[
        'MechaGodzilla',
        '==',
        'Godzilla'
    ],[
        'MechaGodzilla',
        '==',
        'Mothra'
    ]] 
}
start = clock()
results = BacktrackSearch(csp)
for monster, place in results.iteritems():
    print "%15s lives in %s" % (monster, place)
print "Nodes searched: %d" % NODES_SEARCHED
print "Finished in %5.3f seconds" % (clock()-start)
