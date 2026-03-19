# Boolean Engine (V1)
Custom Python Library For Boolean Logic Solvers and Truth Table Operations


## Features
- [Boolean Engine (V1)](#boolean-engine-v1)
  - [Features](#features)
    - [Truthtable Generation](#truthtable-generation)
    - [SAT Solvers](#sat-solvers)
      - [CNF Parser](#cnf-parser)
      - [k-SAT Solver](#k-sat-solver)
      - [2-SAT Solver](#2-sat-solver)


---

### Truthtable Generation
Display a formatted truthtable to console with boolean expressions
[`src/truthtables`](src/truthtables.py)
- pass a list of expressions
  - extract & display the variables
  - extract & display the subexpressions
- pass a list of variables and expressions
  - display variables from list
  - extract & display subexpressions of listed variables

run testcases:
`python src/truthtables.py`


---

### SAT Solvers

#### CNF Parser
[`src/cnf_ksat`](src/cnf_ksat.py)
- a string representing of the expression is passed to the parser
  - each expression made up of a product (disjunction) of clauses
  - each clause made up of a sum (conjunction) of literals
  - each literal is a variable or its complement
- returns an assignment/mapping of variables to boolean values such that the expression evaluates to True (or 1)

#### k-SAT Solver
Solves k-SAT problem using dynamic programming to generate a candidate assignment and prove satisfiability.
Generates a viable assignment of variables to boolean values
[`src/cnf_ksat`](src/cnf_ksat.py)

run tests:
`python src/cnf_ksat.py`
run custom expression:
`python src/cnf_ksat.py -e "<cnf expression>"`


#### 2-SAT Solver
Solves 2SAT problem in linear time using implication graph
Based on the algorithm by Aspvall–Plass–Tarjan.
[`src/cnf_2sat`](src/cnf_2sat.py)

run tests:
`python src/cnf_2sat.py`
run custom expression:
`python src/cnf_ksat.py -e "<2sat expression>"`

---

