import random
import time
import copy

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 40
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# i feel if i don't preview, i can't catch up with this course. Lots of material.

#####################################################
#####################################################


# A clause consists of a set of symbols, each of which is negated
# or not. A clause where
# clause.symbols = {"a": 1, "b": -1, "c": 1}
# corresponds to the statement: a OR (NOT b) OR c .
class Clause:
    def __init__(self):
        pass

    def from_str(self, s):
        s = s.split()
        self.symbols = {}
        for token in s:
            if token[0] == "-":
                sign = -1
                symbol = token[1:]
            else:
                sign = 1
                symbol = token
            self.symbols[symbol] = sign

    def __str__(self):
        tokens = []
        for symbol,sign in self.symbols.items():
            token = ""
            if sign == -1:
                token += "-"
            token += symbol
            tokens.append(token)
        return " ".join(tokens)

# A SAT instance consists of a set of CNF clauses. All clauses
# must be satisfied in order for the SAT instance to be satisfied.


class SatInstance:
    def __init__(self):
        pass

    def from_str(self, s):
        self.symbols = set()
        self.clauses = []
        for line in s.splitlines():
            clause = Clause()
            clause.from_str(line)
            self.clauses.append(clause)
            for symbol in clause.symbols:
                self.symbols.add(symbol)
        self.symbols = sorted(self.symbols)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s

    # Takes as input an assignment to symbols and returns True or
    # False depending on whether the instance is satisfied.
    # Input:
    # - assignment: Dictionary of the format {symbol: sign}, where sign
    #       is either 1 or -1.
    # Output: True or False
    def is_satisfied(self, assignment):
        for symbol in self.symbols:
            if symbol not in assignment:
                return False

        s=copy.deepcopy(self.clauses)
        for clause in s:
            for clause_symbol in clause.symbols:
                clause.symbols[clause_symbol]=assignment[clause_symbol]*clause.symbols[clause_symbol]
        for clause in s:
            if any(x!=-1 for x in clause.symbols.values())==False:
                return False
        return True

    def unsatisfied(self, assignment):

        for clause in self.clauses:
            f = False
            for symbol in clause.symbols:
                if symbol not in assignment:
                    f = True
                    break

            if f != True:
                value = False
                for symbol in clause.symbols:
                    if clause.symbols[symbol]*assignment[symbol] == 1:
                        value = True
                        break
                if value == False:
                    return True

        return False
    
    def unsigned(self, assignment):
         for symbol in self.symbols:
             if symbol not in assignment:
                 return symbol

    def pure_eliminate(self, assignment):
        rest=[]
        for clause in self.clauses:
            f = False
            for clause_symbol in clause.symbols:
                if clause_symbol in assignment:
                    if assignment[clause_symbol]*clause.symbols[clause_symbol] == 1:
                        f = True
                        break

            if f == False:
                rest.append(clause)

        symbol_value={}
        
        for clause in rest:
            for clause_symbol in clause.symbols:
                if clause_symbol not in assignment:
                    if clause_symbol not in symbol_value:
                        symbol_value[clause_symbol] = clause.symbols[clause_symbol]
                    if symbol_value[clause_symbol] != clause.symbols[clause_symbol]:
                        symbol_value[clause_symbol] = 0
                        
        for symbol in symbol_value:
            if symbol_value[symbol] == 0:
                return [-1,-1]
            if symbol_value[symbol]==-1:
                return [symbol,symbol_value[symbol]]
        return [-1,-1]

  
    def unit_propogate(self, assignment):

        for clause in self.clauses:
            if len(clause.symbols)==1:
                symbol = clause.symbols.keys()[0]
                if symbol not in assignment:
                    return [symbol,clause.symbols[symbol]]
                
        for clause in self.clauses:
            unit=[]
            unassigned = 0
            f = 0
            for clause_symbol in clause.symbols:
                if unassigned != 0 and clause_symbol not in assignment:
                    unassigned += 1
                    break
                    unit.append(clause.symbols[clause_symbol])
                    
                elif unassigned == 0 and clause_symbol not in assignment:
                    unassigned += 1
                    unit.append(clause_symbol)
                    unit.append(clause.symbols[clause_symbol])
                    
                elif assignment[clause_symbol]*clause.symbols[clause_symbol] == 1:
                    f = 1
                    break

            if unassigned==1 and f==0:
                return unit
            
        return [-1,-1]




# Find correct assignment to SatInstance using DPLL with backtracking and some heuristics
# Input:
#  - instance: SAT instance
#  - assignment: Dictionary of the format {symbol: sign}, where sign
#       is either 1 or -1.
# Output:
#   True or false



assignment=()
def dpll(instance):
    global assignment

    if instance.is_satisfied(assignment):
        return True
    if instance.unsatisfied(assignment):
        return False
    # do unit propogate
    [symbol,value] = instance.unit_propogate(assignment)
    if symbol!=-1:
        assignment.update({symbol: value})
        return dpll(instance)
    # do pure_elimination
    [symbol,value] = instance.pure_eliminate(assignment)
    if symbol!=-1:
        assignment.update({symbol: value})
        return dpll(instance)
    # copy the current assignment and find unassigned one
    rest=copy.deepcopy(assignment)
    unsigned = instance.unsigned(assignment)
    #find unsigned one , assign -1 or 1
    assignment.update({unsigned: -1})
    if dpll(instance)!=True:
        assignment = rest
        assignment.update({unsigned: 1})
        return dpll(instance)
    else:
        return True


# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: SAT instance
# - assignment: Dictionary of the format {symbol: sign}, where sign
#       is either 1 or -1.



def solve_dpll(instance):
    global assignment
    assignment={}
    if dpll(instance) == True:
        return assignment


    
with open("big_instances.txt", "r") as input_file:
     instance_strs = input_file.read()

instance_strs = instance_strs.split("\n\n")

with open("big_assignments.txt", "w") as output_file:
    for instance_str in instance_strs:
        instance = SatInstance()
        instance.from_str(instance_str)
        assignment = solve_dpll(instance)
        for symbol_index, (symbol,sign) in enumerate(assignment.items()):
            if symbol_index != 0:
                output_file.write(" ")
            token = ""
            if sign == -1:
                token += "-"
            token += symbol
            output_file.write(token)
        output_file.write("\n")


