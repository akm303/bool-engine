# Boolean Engine (V2)
Custom Python Library For Boolean Logic Solvers and Truth Table Operations

`main.py`, currently all operations must be invoked directly from each script.
eg. to run a 2sat solver, must invoke `python -m src.solver.cnf_2sat.py -e "<some 2cnf expression>"`



## Features
- [Boolean Engine (V2)](#boolean-engine-v2)
  - [Features](#features)
    - [Truthtable Generation](#truthtable-generation)
    - [SAT Solvers](#sat-solvers)
      - [k-SAT Solvers](#k-sat-solvers)
      - [2-SAT Solvers](#2-sat-solvers)
  - [Testing](#testing)
  - [Utils](#utils)
      - [CNF Parser](#cnf-parser)
  - [Project Architecture](#project-architecture)


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

run local tests: `python src.structures.truthtables.py`
run custom inputs: wip

---

### SAT Solvers

#### k-SAT Solvers
Solves k-SAT problem using dynamic programming to generate a candidate assignment and prove satisfiability.  
Generates a viable assignment of variables to boolean values  
[`src/solvers/cnf_ksat`](src/solvers/cnf_ksat.py)  

run local tests: `python -m src.solver.cnf_ksat`  
run custom inputs: `python -m src.solver.cnf_ksat -e "<cnf expression>"`  


#### 2-SAT Solvers
Solves 2SAT problem in linear time using implication graph  
- [`Custom Algorithm (src/solvers/cnf_2sat)`](src/solvers/cnf_2sat.py)  
- [Apsvall, Plass, Tarjan's Algorithm (`src/solvers/cnf_apt`)](src/solvers/cnf_apt.py)  
- [DP Algorithm (`src/solvers/dp_2sat`)](src/solvers/dp_2sat.py)  

run local tests: `python -m src.solver.cnf_2sat`    
run custom inputs: `python -m src.solver.cnf_2sat -e "<2cnf expression>`    


---
## Testing
`src/testing.py` - custom global testing scripts for each solver, utility, and structure

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


---
## Project Architecture
```
├── src
│   ├── solver
│   │   ├── cnf_2sat.py
│   │   ├── cnf_apt.py
│   │   ├── cnf_ksat.py
│   │   └── dp_2sat.py
│   ├── structure
│   │   ├── gates.py
│   │   ├── implication_graph.py
│   │   ├── ksat.py
│   │   ├── parsers.py
│   │   └── truthtables.py
│   ├── tests
│   ├── utils
│   │   ├── expressions.py
│   │   ├── syntax.py
│   │   ├── tester.py
│   │   └── transforms.py
│   ├── common.py
│   └── testing.py
├── main.py
├── pyproject.toml
├── readme.md
└── setup.py

6 directories, 19 files
```

