from collections import defaultdict
from functools import reduce


class CSP():
   
    def __init__(self, variables, domains, neighbors, constraints):
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0
    #Add {var: val}
    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1
    #Remove {var: val}
    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    #Return the number of conflicts var=val has with other variables
    def nconflicts(self, var, val, assignment):
        
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        return count(conflict(v) for v in self.neighbors[var])
        
    def goal_test(self, state):
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))
    #if the current domain list is empty then start from the beginning and make current domain equal to the main domain dict
    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}
    #create removal list , see if for certain var if value is in the current domain or not if not then add it to the removal
    def suppose(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals
    #remove value of certain var in the current domain list and add it in the removal list
    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))
   # Return all values for var that aren't currently ruled
    def choices(self, var):
        return (self.curr_domains or self.domains)[var]
    #return values of var from removal list to current domain list
    def restore(self, removals):
       
        for B, b in removals:
            self.curr_domains[B].append(b)

# ______________________________________________________________________________
# CSP Backtracking Search

# Variable ordering

def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(bool(x) for x in seq)
