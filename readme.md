# Boolean Engine (V2)
Custom Python Library For Boolean Logic Solvers and Truth Table Operations

`main.py`, currently all operations must be invoked directly from each script.
eg. to run a 2sat solver, must invoke `python -m src.solver.cnf_2sat.py -e "<some 2cnf expression>"`



## Features
- [Boolean Engine (V2)](#boolean-engine-v2)
  - [Features](#features)
    - [Truthtable Generation](#truthtable-generation)
    - [SAT Solvers](#sat-solvers)
      - [k-SAT Solver](#k-sat-solver)
      - [2-SAT Solver](#2-sat-solver)
  - [Testing](#testing)
  - [Utils](#utils)
      - [CNF Parser](#cnf-parser)


---

### Truthtable Generation
Display a formatted truthtable to console with boolean expressions
[`src.structures.truthtables`](src/truthtables.py)
- pass a list of expressions
  - extract & display the variables
  - extract & display the subexpressions
- pass a list of variables and expressions
  - display variables from list
  - extract & display subexpressions of listed variables

run testcases:
`python src.structures.truthtables.py`


---

### SAT Solvers

#### k-SAT Solver
Solves k-SAT problem using dynamic programming to generate a candidate assignment and prove satisfiability.  
Generates a viable assignment of variables to boolean values  
[`src/solvers/cnf_ksat`](src/solvers/cnf_ksat.py)  

run tests: `python src/cnf_ksat.py`  
run custom: `python src/cnf_ksat.py -e "<cnf expression>"`  


#### 2-SAT Solver
Solves 2SAT problem in linear time using implication graph  
- [`src/solvers/cnf_2sat`](src/solvers/cnf_2sat.py)  
- [`src/solvers/cnf_apt`](src/solvers/cnf_apt.py)  
- [`src/solvers/dp_2sat`](src/solvers/dp_2sat.py)  

run tests: `python -m src.solver.cnf_2sat`    
<!-- run tests: `python src/cnf_2sat.py`   -->
run tests: `python -m src.solver.cnf_2sat -e "<2sat expression>`    
run custom: `python src/cnf_ksat.py -e "<2sat expression>"`  

---
## Testing
`src/testing.py` - custom testing scripts for each solver, utility, and structure

run all tests: `python -m src.testing`  



---
## Utils
#### CNF Parser
[`src/structures/parsers`](src/structures/parsers.py)
- a string representing of the expression is passed to the parser
  - each expression made up of a product (disjunction) of clauses
  - each clause made up of a sum (conjunction) of literals
  - each literal is a variable or its complement
- returns an assignment/mapping of variables to boolean values such that the expression evaluates to True (or 1)


