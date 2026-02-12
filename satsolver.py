# from truthtables import *

# def propositional

# def toCNF(expression):


class Expression:
    def __init__(self, cnf_expression:str):
        self.expression = cnf_expression
        self.literals = []
        self.operations = []
        self.parse()

    def parse(self):
        expression = self.expression


class Problem:
    """
    Abstract Problem Class
    """
    def __init__(self):
        pass

class SAT(Problem):
    """
    SAT Problem
    """
    def __init__(self):
        self.expression = None


class Solver:
    def __init__(self,problem,algorithm,autorun = False):
        self.problem = problem
        self.algorithm = algorithm
        if autorun:
            self.solution = self.solve()
    
    def solve(self):
        self.algorithm(self.problem)


def expression_test():
    cnf_e1 = ""
    e1 = Expression()

def sat_test():
    pass

def solver_test():
    pass


if __name__ == "__main__":
    expression_test()
    sat_test()
    solver_test()