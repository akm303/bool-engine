importing `implication_graph.py`
importing `cnf_2sat.py`
running `testing.py

## running: `tester_test()`
----------------------------------------
```tex
----------------------------------------
TESTER TEST (META)
----------------------------------------
generating test from collection:

test is set up: TESTER RUN 1:
cases: [Test Case 0, Test Case 1, Test Case 2, Test Case 3, Test Case 4, Test Case 5, Test Case 6, Test Case 7, Test Case 8]
allpass? False
passing: []
failing: []
> (Pre Run Check) Passed

test running...

test ran: TESTER RUN 1:
cases: [Test Case 0, Test Case 1, Test Case 2, Test Case 3, Test Case 4, Test Case 5, Test Case 6, Test Case 7, Test Case 8]
allpass? True
passing: ['Test Case 0: (0, 0)', 'Test Case 1: (1, 0)', 'Test Case 2: (2, 0)', 'Test Case 3: (0, 1)', 'Test Case 4: (1, 1)', 'Test Case 5: (2, 1)', 'Test Case 6: (0, 2)', 'Test Case 7: (1, 2)', 'Test Case 8: (2, 2)']
failing: []
> (Post Run Check) Passed

----------------------------------------

generating test from collection:

test is set up: TESTER RUN 2:
cases: [Test Case 9, Test Case 10, Test Case 11, Test Case 12, Test Case 13, Test Case 14, Test Case 15, Test Case 16, Test Case 17]
allpass? False
passing: []
failing: []
> (Pre Run Check) Passed

test running...

test ran: TESTER RUN 2:
cases: [Test Case 9, Test Case 10, Test Case 11, Test Case 12, Test Case 13, Test Case 14, Test Case 15, Test Case 16, Test Case 17]
allpass? False
passing: ['Test Case 10: (1, 0)', 'Test Case 11: (2, 0)', 'Test Case 12: (0, 1)', 'Test Case 13: (1, 1)', 'Test Case 14: (2, 1)', 'Test Case 15: (0, 2)', 'Test Case 16: (1, 2)', 'Test Case 17: (2, 2)']
failing: ['Test Case 9: (0, 0)']
> (Post Run Check) Passed

----------------------------------------

generating test from collection:

test is set up: TESTER RUN 3:
cases: [Test Case 18, Test Case 19, Test Case 20, Test Case 21, Test Case 22, Test Case 23, Test Case 24, Test Case 25, Test Case 26]
allpass? False
passing: []
failing: []
> (Pre Run Check) Passed

test running...

test ran: TESTER RUN 3:
cases: [Test Case 18, Test Case 19, Test Case 20, Test Case 21, Test Case 22, Test Case 23, Test Case 24, Test Case 25, Test Case 26]
allpass? False
passing: ['Test Case 19: (1, 0)', 'Test Case 20: (2, 0)', 'Test Case 21: (0, 1)', 'Test Case 22: (1, 1)', 'Test Case 23: (2, 1)', 'Test Case 24: (0, 2)', 'Test Case 25: (1, 2)']
failing: ['Test Case 18: (0, 0)', 'Test Case 26: (2, 2)']
> (Post Run Check) Passed

----------------------------------------

Tester Passes


----------------------------------------
`tester_test()` output: 
 >>> True
----------------------------------------

```

----------------------------------------
## completed: `tester_test()`


## running: Syntax [To Local]
----------------------------------------
```tex


----------------------------------------
Syntax [To Local] output: 
 >>> All Passed
----------------------------------------

```

----------------------------------------
## completed: Syntax [To Local]


## running: Helper Function: to_2sat()
----------------------------------------
```tex


----------------------------------------
Helper Function: to_2sat() output: 
 >>> All Passed
----------------------------------------

```

----------------------------------------
## completed: Helper Function: to_2sat()


## running: 2SAT Solver
----------------------------------------
```tex
----------------------------------------
2-SAT Solver (custom)
expression  :: "(X+Y)"
     clauses = [(X + Y)]
    literals = [X, Y]
   variables = [X, Y]

nodes: [X , Y , X', Y']
edges: [( X', Y ), ( Y', X )]
graph (adjacency): {
  X : {},
  Y : {},
  X': {Y },
  Y': {X }
}

  reachable from X : [X ]
  reachable from X': [X', Y ]
  reachable from Y : [Y ]
  reachable from Y': [Y', X ]
is satisfiable? True
----------------------------------------

----------------------------------------
2-SAT Solver (custom)
expression  :: "(X+Y')"
     clauses = [(X + Y')]
    literals = [X, Y']
   variables = [X, Y]

nodes: [X , Y , X', Y']
edges: [( X', Y'), ( Y , X )]
graph (adjacency): {
  X : {},
  Y : {X },
  X': {Y'},
  Y': {}
}

  reachable from X : [X ]
  reachable from X': [X', Y']
  reachable from Y : [Y , X ]
  reachable from Y': [Y']
is satisfiable? True
----------------------------------------

----------------------------------------
2-SAT Solver (custom)
expression  :: "(X'+Y)"
     clauses = [(X' + Y)]
    literals = [X', Y]
   variables = [X, Y]

nodes: [X , Y , X', Y']
edges: [( X , Y ), ( Y', X')]
graph (adjacency): {
  X : {Y },
  Y : {},
  X': {},
  Y': {X'}
}

  reachable from X : [X , Y ]
  reachable from X': [X']
  reachable from Y : [Y ]
  reachable from Y': [Y', X']
is satisfiable? True
----------------------------------------

----------------------------------------
2-SAT Solver (custom)
expression  :: "(X'+Y')"
     clauses = [(X' + Y')]
    literals = [X', Y']
   variables = [X, Y]

nodes: [X , Y , X', Y']
edges: [( X , Y'), ( Y , X')]
graph (adjacency): {
  X : {Y'},
  Y : {X'},
  X': {},
  Y': {}
}

  reachable from X : [X , Y']
  reachable from X': [X']
  reachable from Y : [Y , X']
  reachable from Y': [Y']
is satisfiable? True
----------------------------------------

----------------------------------------
2-SAT Solver (custom)
expression  :: "(X+Y)(X'+Y)"
     clauses = [(X + Y), (X' + Y)]
    literals = [X, X', Y]
   variables = [X, Y]

nodes: [X , Y , X', Y']
edges: [( X', Y ), ( Y', X ), ( X , Y ), ( Y', X')]
graph (adjacency): {
  X : {Y },
  Y : {},
  X': {Y },
  Y': {X', X }
}

  reachable from X : [X , Y ]
  reachable from X': [X', Y ]
  reachable from Y : [Y ]
  reachable from Y': [Y', X', Y , X ]
is satisfiable? True
----------------------------------------

----------------------------------------
2-SAT Solver (custom)
expression  :: "(X+Y)(X'+Y')"
     clauses = [(X + Y), (X' + Y')]
    literals = [X, X', Y, Y']
   variables = [X, Y]

nodes: [X , Y , X', Y']
edges: [( X', Y ), ( Y', X ), ( X , Y'), ( Y , X')]
graph (adjacency): {
  X : {Y'},
  Y : {X'},
  X': {Y },
  Y': {X }
}

  reachable from X : [X , Y']
  reachable from X': [X', Y ]
  reachable from Y : [Y , X']
  reachable from Y': [Y', X ]
is satisfiable? True
----------------------------------------

----------------------------------------
2-SAT Solver (custom)
expression  :: "(x_1'+x_2)(x_1'+x_3)"
     clauses = [(x_1' + x_2), (x_1' + x_3)]
    literals = [x_1', x_2, x_3]
   variables = [x_1, x_2, x_3]

nodes: [x_1 , x_2 , x_3 , x_1', x_2', x_3']
edges: [( x_1 , x_2 ), ( x_2', x_1'), ( x_1 , x_3 ), ( x_3', x_1')]
graph (adjacency): {
  x_1 : {x_3 , x_2 },
  x_2 : {},
  x_3 : {},
  x_1': {},
  x_2': {x_1'},
  x_3': {x_1'}
}

  reachable from x_1 : [x_1 , x_3 , x_2 ]
  reachable from x_1': [x_1']
  reachable from x_2 : [x_2 ]
  reachable from x_2': [x_2', x_1']
  reachable from x_3 : [x_3 ]
  reachable from x_3': [x_3', x_1']
is satisfiable? True
----------------------------------------

----------------------------------------
2-SAT Solver (custom)
expression  :: "(x_1'+x_2)(x_2'+x_3)(x_3+x_2)(x_3'+x_1')"
     clauses = [(x_1' + x_2), (x_2' + x_3), (x_3 + x_2), (x_3' + x_1')]
    literals = [x_1', x_2, x_2', x_3, x_3']
   variables = [x_1, x_2, x_3]

nodes: [x_1 , x_2 , x_3 , x_1', x_2', x_3']
edges: [( x_1 , x_2 ), ( x_2', x_1'), ( x_2 , x_3 ), ( x_3', x_2'), ( x_3', x_2 ), ( x_2', x_3 ), ( x_3 , x_1'), ( x_1 , x_3')]
graph (adjacency): {
  x_1 : {x_3', x_2 },
  x_2 : {x_3 },
  x_3 : {x_1'},
  x_1': {},
  x_2': {x_3 , x_1'},
  x_3': {x_2 , x_2'}
}

  reachable from x_1 : [x_1 , x_3', x_2 , x_3 , x_1', x_2']
  reachable from x_1': [x_1']
  reachable from x_2 : [x_2 , x_3 , x_1']
  reachable from x_2': [x_2', x_3 , x_1']
  reachable from x_3 : [x_3 , x_1']
  reachable from x_3': [x_3', x_2 , x_3 , x_1', x_2']
is satisfiable? True
----------------------------------------

----------------------------------------
2-SAT Solver (custom)
expression  :: "(x_1'+x_2)(x_2'+x_3)(x_3+x_2)(x_3'+x_1')(x_3'+x_1)"
     clauses = [(x_1' + x_2), (x_2' + x_3), (x_3 + x_2), (x_3' + x_1'), (x_3' + x_1)]
    literals = [x_1, x_1', x_2, x_2', x_3, x_3']
   variables = [x_1, x_2, x_3]

nodes: [x_1 , x_2 , x_3 , x_1', x_2', x_3']
edges: [( x_1 , x_2 ), ( x_2', x_1'), ( x_2 , x_3 ), ( x_3', x_2'), ( x_3', x_2 ), ( x_2', x_3 ), ( x_3 , x_1'), ( x_1 , x_3'), ( x_3 , x_1 ), ( x_1', x_3')]
graph (adjacency): {
  x_1 : {x_3', x_2 },
  x_2 : {x_3 },
  x_3 : {x_1 , x_1'},
  x_1': {x_3'},
  x_2': {x_3 , x_1'},
  x_3': {x_2 , x_2'}
}

  reachable from x_1 : [x_1 , x_3', x_2 , x_3 , x_1', x_2']
  reachable from x_1': [x_1', x_3', x_2 , x_3 , x_1 , x_2']
 ! found bidirectional paths between [ x_1  <=> x_1' ]
  reachable from x_2 : [x_2 , x_3 , x_1 , x_3', x_2', x_1']
  reachable from x_2': [x_2', x_3 , x_1 , x_3', x_2 , x_1']
 ! found bidirectional paths between [ x_2  <=> x_2' ]
  reachable from x_3 : [x_3 , x_1 , x_3', x_2 , x_2', x_1']
  reachable from x_3': [x_3', x_2 , x_3 , x_1 , x_1', x_2']
 ! found bidirectional paths between [ x_3  <=> x_3' ]
is satisfiable? False
evidence: paths exist between [('x_1', "x_1'"), ('x_2', "x_2'"), ('x_3', "x_3'")]
----------------------------------------

----------------------------------------
2-SAT Solver (custom)
expression  :: "(x_2'+x_1)(x_1'+x_3)(x_3+x_1)(x_3'+x_2')(x_3'+x_2)"
     clauses = [(x_2' + x_1), (x_1' + x_3), (x_3 + x_1), (x_3' + x_2'), (x_3' + x_2)]
    literals = [x_1, x_1', x_2, x_2', x_3, x_3']
   variables = [x_1, x_2, x_3]

nodes: [x_1 , x_2 , x_3 , x_1', x_2', x_3']
edges: [( x_2 , x_1 ), ( x_1', x_2'), ( x_1 , x_3 ), ( x_3', x_1'), ( x_3', x_1 ), ( x_1', x_3 ), ( x_3 , x_2'), ( x_2 , x_3'), ( x_3 , x_2 ), ( x_2', x_3')]
graph (adjacency): {
  x_1 : {x_3 },
  x_2 : {x_1 , x_3'},
  x_3 : {x_2 , x_2'},
  x_1': {x_3 , x_2'},
  x_2': {x_3'},
  x_3': {x_1 , x_1'}
}

  reachable from x_1 : [x_1 , x_3 , x_2 , x_3', x_1', x_2']
  reachable from x_1': [x_1', x_3 , x_2 , x_1 , x_3', x_2']
 ! found bidirectional paths between [ x_1  <=> x_1' ]
  reachable from x_2 : [x_2 , x_1 , x_3 , x_2', x_3', x_1']
  reachable from x_2': [x_2', x_3', x_1 , x_3 , x_2 , x_1']
 ! found bidirectional paths between [ x_2  <=> x_2' ]
  reachable from x_3 : [x_3 , x_2 , x_1 , x_3', x_1', x_2']
  reachable from x_3': [x_3', x_1 , x_3 , x_2 , x_2', x_1']
 ! found bidirectional paths between [ x_3  <=> x_3' ]
is satisfiable? False
evidence: paths exist between [('x_1', "x_1'"), ('x_2', "x_2'"), ('x_3', "x_3'")]
----------------------------------------

----------------------------------------
2-SAT Solver (custom)
expression  :: "(x_3'+x_2)(x_2'+x_1)(x_1+x_2)(x_1'+x_3')(x_1'+x_3)"
     clauses = [(x_3' + x_2), (x_2' + x_1), (x_1 + x_2), (x_1' + x_3'), (x_1' + x_3)]
    literals = [x_1, x_1', x_2, x_2', x_3, x_3']
   variables = [x_1, x_2, x_3]

nodes: [x_1 , x_2 , x_3 , x_1', x_2', x_3']
edges: [( x_3 , x_2 ), ( x_2', x_3'), ( x_2 , x_1 ), ( x_1', x_2'), ( x_1', x_2 ), ( x_2', x_1 ), ( x_1 , x_3'), ( x_3 , x_1'), ( x_1 , x_3 ), ( x_3', x_1')]
graph (adjacency): {
  x_1 : {x_3', x_3 },
  x_2 : {x_1 },
  x_3 : {x_1', x_2 },
  x_1': {x_2 , x_2'},
  x_2': {x_3', x_1 },
  x_3': {x_1'}
}

  reachable from x_1 : [x_1 , x_3', x_1', x_2 , x_2', x_3 ]
  reachable from x_1': [x_1', x_2 , x_1 , x_3', x_3 , x_2']
 ! found bidirectional paths between [ x_1  <=> x_1' ]
  reachable from x_2 : [x_2 , x_1 , x_3', x_1', x_2', x_3 ]
  reachable from x_2': [x_2', x_3', x_1', x_2 , x_1 , x_3 ]
 ! found bidirectional paths between [ x_2  <=> x_2' ]
  reachable from x_3 : [x_3 , x_1', x_2 , x_1 , x_3', x_2']
  reachable from x_3': [x_3', x_1', x_2 , x_1 , x_3 , x_2']
 ! found bidirectional paths between [ x_3  <=> x_3' ]
is satisfiable? False
evidence: paths exist between [('x_1', "x_1'"), ('x_2', "x_2'"), ('x_3', "x_3'")]
----------------------------------------

----------------------------------------
2-SAT Solver (custom)
expression  :: "(x_a'+x_a)"
     clauses = [(x_a' + x_a)]
    literals = [x_a, x_a']
   variables = [x_a]

nodes: [x_a , x_a']
edges: [( x_a , x_a ), ( x_a', x_a')]
graph (adjacency): {
  x_a : {x_a },
  x_a': {x_a'}
}

  reachable from x_a : [x_a ]
  reachable from x_a': [x_a']
is satisfiable? True
----------------------------------------

----------------------------------------
2-SAT Solver (custom)
expression  :: "(A+A)(A'+A')"
     clauses = [(A + A), (A' + A')]
    literals = [A, A']
   variables = [A]

nodes: [A , A']
edges: [( A', A ), ( A', A ), ( A , A'), ( A , A')]
graph (adjacency): {
  A : {A'},
  A': {A }
}

  reachable from A : [A , A']
  reachable from A': [A', A ]
 ! found bidirectional paths between [ A  <=> A' ]
is satisfiable? False
evidence: paths exist between [('A', "A'")]
----------------------------------------



----------------------------------------
2SAT Solver output: 
 >>> All Passed
----------------------------------------

```

----------------------------------------
## completed: 2SAT Solver


## running: kSAT Solver
----------------------------------------
```tex
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
kSAT Solver output: 
 >>> All Passed
----------------------------------------

```

----------------------------------------
## completed: kSAT Solver


All tests passed
