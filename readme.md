# Boolean Logic (V1)
Custom Python Library For Implmentation Of Boolean Logic and Truth Table Operations


## Features
- [Boolean Logic (V1)](#boolean-logic-v1)
  - [Features](#features)
    - [Truthtable Generation](#truthtable-generation)
    - [SAT Solver](#sat-solver)


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

### SAT Solver
Solves SAT problem for any boolean equation in CNF form equal to 1 (v1)
[`src/sat`](src/sat.py)
- pass a string representing the expression
  - each expression made up of a product (disjunction) of clauses
  - each clause made up of a sum (conjunction) of literals
  - each literal is a variable or its complement
- returns an assignment/mapping of variables to boolean values such that the expression evaluates to True (or 1)

run testcases:
`python src/sat.py`


---

