importing `common.py
running `cnf_ksat.py`

----------------------------------------
k-SAT Solver
expression  :: "(A)"
     clauses = [(A)]
    literals = [A]
   variables = [A]

is satisfiable? True
solution: { A : 1 }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(A')"
     clauses = [(A')]
    literals = [A']
   variables = [A]

is satisfiable? True
solution: { A : 0 }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(A)(A')"
     clauses = [(A), (A')]
    literals = [A, A']
   variables = [A]

is satisfiable? False
solution: { }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(X+Y)"
     clauses = [(X + Y)]
    literals = [X, Y]
   variables = [X, Y]

is satisfiable? True
solution: { X : 1 , Y : * }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(X+Y')"
     clauses = [(X + Y')]
    literals = [X, Y']
   variables = [X, Y]

is satisfiable? True
solution: { X : 1 , Y : * }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(X'+Y)"
     clauses = [(X' + Y)]
    literals = [X', Y]
   variables = [X, Y]

is satisfiable? True
solution: { X : 1 , Y : 1 }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(X'+Y')"
     clauses = [(X' + Y')]
    literals = [X', Y']
   variables = [X, Y]

is satisfiable? True
solution: { X : 1 , Y : 0 }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(X+Y)(X'+Y)"
     clauses = [(X + Y), (X' + Y)]
    literals = [X, X', Y]
   variables = [X, Y]

is satisfiable? True
solution: { X : 1 , Y : 1 }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(X+Y)(X'+Y')"
     clauses = [(X + Y), (X' + Y')]
    literals = [X, X', Y, Y']
   variables = [X, Y]

is satisfiable? True
solution: { X : 1 , Y : 0 }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(x_1'+x_2)(x_1'+x_3)"
     clauses = [(x_1' + x_2), (x_1' + x_3)]
    literals = [x_1', x_2, x_3]
   variables = [x_1, x_2, x_3]

is satisfiable? True
solution: { x_1 : 1 , x_2 : 1 , x_3 : 1 }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(x_1'+x_2+x_4')(x_2+x_3'+x_4)(x_1+x_2'+x_3)(x_1+x_2+x_3)"
     clauses = [(x_1' + x_2 + x_4'), (x_2 + x_3' + x_4), (x_1 + x_2' + x_3), (x_1 + x_2 + x_3)]
    literals = [x_1, x_1', x_2, x_2', x_3, x_3', x_4, x_4']
   variables = [x_1, x_2, x_3, x_4]

is satisfiable? True
solution: { x_1 : 1 , x_2 : 1 , x_3 : * , x_4 : * }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(x_1'+x_2'+x_4'+x_5')(x_2'+x_3+x_5'+x_6')(x_1+x_2+x_3+x_5)"
     clauses = [(x_1' + x_2' + x_4' + x_5'), (x_2' + x_3 + x_5' + x_6'), (x_1 + x_2 + x_3 + x_5)]
    literals = [x_1, x_1', x_2, x_2', x_3, x_4', x_5, x_5', x_6']
   variables = [x_1, x_2, x_3, x_4, x_5, x_6]

is satisfiable? True
solution: { x_1 : 1 , x_2 : 1 , x_3 : 1 , x_4 : 1 , x_5 : 0 , x_6 : * }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(x_1'+x_2)(x_2'+x_3)(x_3+x_2)(x_3'+x_1')"
     clauses = [(x_1' + x_2), (x_2' + x_3), (x_3 + x_2), (x_3' + x_1')]
    literals = [x_1', x_2, x_2', x_3, x_3']
   variables = [x_1, x_2, x_3]

is satisfiable? True
solution: { x_1 : 0 , x_2 : 1 , x_3 : 1 }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(x_1'+x_2)(x_2'+x_3)(x_3+x_2)(x_3'+x_1')(x_3'+x_1)"
     clauses = [(x_1' + x_2), (x_2' + x_3), (x_3 + x_2), (x_3' + x_1'), (x_3' + x_1)]
    literals = [x_1, x_1', x_2, x_2', x_3, x_3']
   variables = [x_1, x_2, x_3]

is satisfiable? False
solution: { }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(x_2'+x_1)(x_1'+x_3)(x_3+x_1)(x_3'+x_2')(x_3'+x_2)"
     clauses = [(x_2' + x_1), (x_1' + x_3), (x_3 + x_1), (x_3' + x_2'), (x_3' + x_2)]
    literals = [x_1, x_1', x_2, x_2', x_3, x_3']
   variables = [x_1, x_2, x_3]

is satisfiable? False
solution: { }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(x_a'+x_1)(x_1'+x_3)(x_3+x_1)(x_3'+x_a')(x_3'+x_a)"
     clauses = [(x_a' + x_1), (x_1' + x_3), (x_3 + x_1), (x_3' + x_a'), (x_3' + x_a)]
    literals = [x_1, x_1', x_3, x_3', x_a, x_a']
   variables = [x_1, x_3, x_a]

is satisfiable? False
solution: { }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(x_a'+x_a)"
     clauses = [(x_a' + x_a)]
    literals = [x_a, x_a']
   variables = [x_a]

is satisfiable? True
solution: { x_a : 1 }
----------------------------------------

----------------------------------------
k-SAT Solver
expression  :: "(A+A)(A'+A')"
     clauses = [(A + A), (A' + A')]
    literals = [A, A']
   variables = [A]

is satisfiable? False
solution: { }
----------------------------------------

