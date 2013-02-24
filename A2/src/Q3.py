###############################################################################
#Q3.py 
#CMPT 317 A2
#Quinn Neumiiller
#11065618
#qjn162
###############################################################################
#IMPORTS
###############################################################################

###############################################################################
#GLOBALS
###############################################################################

Variables = [
    "Godzilla", 
    "Mothra", 
    "Rodan", 
    "MechaGodzilla", 
    "King Kong"
]

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
    #   if assignment is complete then return assignment
    if(assignment):
        return assignment
    #   var <- Select-Unassigned-Variable(csp)
    var = Variables.pop()
    while(True):
        print var
    #   for each value in Order-Domain-Values(var, assignment, csp) do

    #   if value is consistent with assignment then
    #   add{var = value} to assignment
    Assignment.append({})
    #   inferences <- Inference(csp, var, value)
    #   if inferences != failure then
    #   add inferences to assignment
    #   result <- Backtrack(assignment, csp)
    #   if result != faulure then
    #   return result
    #   remove {var = value} and inferences from assignment
    #   return failure
    global Variables
    return csp

###############################################################################
#MAIN
###############################################################################


csp = {
    
}

print BacktrackSearch(csp)