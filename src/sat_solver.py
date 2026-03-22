"""
Goal: Architecture that allows openly running SAT solving algorithms on expressions,  
as well as configuring assertions and checks to validate a run
(eg. 2SAT must run on a expression in CNF with 2-literals per clause) 

runner(problem,solver) -> result
problem = string expression
solver = {algorithm, requirements, result_format}
result = {result_value, evidence}

"""