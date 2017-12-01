# lightsoutpuzzlegame
Implement a solver for the Satisfiability (SAT) problem. In particular, you will implement the Davis–Putnam–Logemann–Loveland (DPLL) algorithm. This algorithm takes as input a logical statement in CNF format and outputs a assignment of True or False to each propositional symbol.

The assignments file has one assignment per line. Each assignment consists of a series of whitespace-separated symbol assignments, where "a" indicates the assignment "a = True" and "-a" indicates "a = False". The instance file is a list of instances, separated by double newlines. Each instance is a list of clauses, separated by newlines. The clause "a -b c" corresponds to the propositional sentence "a OR (not b) OR c". The i-th instance in the input file corresponds to the i-th assignment in the assignment file.

Download big instances here. When you are ready, run your code to generate solutions for these instances. Your code should take less than five minutes to run on this example. Include the output in your submission named big_assignments.txt.

