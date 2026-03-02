in CNF:
- all clauses are ANDed together
- within each clause
  - elements must be literals (either a variable or its complement)
  - elements must be ORed


pseudocode:
1. take expression (in CNF) as input string: 
    Expression E
2. parse expression into clauses: 
    Clauses C_1, C_2, ..., C_k in E
3. extract literals from clauses/expression:
    Literals u_1,u_2,...,u_n in E
        literal u_i refers to either a variable or its complement
4. extract variables x_1,x_2,...,x_n in E
    subset of variables in each clause
5. Domain for each variable is True|False (ie. 1|0)

expressions E
clauses C
variables X

assignment A is mapping of x_i in X to a value from the domain
A is complete when all x_i are mapped to a value

A is consistent/valid if every clause C_i in E evaluates to True (ie. C_i = 1)
    C_i evaluates to True if contains at least one literal that evaluates to True
    (in other words, return 
        any(assignment[x] for x in C_i)
        [assignment[x] for x in C_i]


```example
        expression: (x_1' + x_2 + x_4' + x_5') (x_2 + x_3 + x_5' + x_6') (x_1 + x_2 + x_3 + x_5)
clause 0 variables: [x_1', x_2, x_4', x_5']
clause 1 variables: [x_2, x_3, x_5', x_6']
clause 2 variables: [x_1, x_2, x_3, x_5]
         variables: ['x_1', 'x_2', 'x_3', 'x_4', 'x_5', 'x_6']
```


operational functions:
- extract_clauses(expression)
- extract_variables(expression) (or extract_variables(clause)?)

- evaluate(clause) => boolean
- evaluate(variable) => boolean

- select_variable(variables)


checking functions:
- is_complete(variables, assignment) => boolean
- is_consistent(assignment) => boolean



---

```pseudocode
clauses = extract_clauses(expression)
variables = extract_variables(expression)

assignment = {}
domain = {var:(0,1) for var in variables}
constraints = {var:[all clauses containing var literal]}


def backtrack(variables,domain,assignment):
    if assignment is complete:
        return assignment

    remaining_variables = set(variables) - set(assignment)
    var = select_variable(remaining_variables)
    for val in domain[var]:
        assign(var,val,assignment)

        if is_consistent(assignment):
            result = backtrack(variables,domain,assignment)
            if result isn't none
                return result
            otherwise, remove assignment[var]=val
    otherwise, all assignments failed, so return none 



def is_consistent(var,assignment,constraints)
    /* 
    for assignment to be consistent, each clause containing assigned variable must either
    - not yet be evaluatable (missing some variable assignments)
    - evaluate to True (ie. any(value(literal) == 1 for any literal in C))
    */
    clauses = constraints[var] //each var holds list of clauses
    eval_result = [evaluate_clause(var,assignment,clauses) for clause in clauses]
    
        





```