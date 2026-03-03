import re
from pprint import pformat

# ------------------------------ #

a0=None
am=None
N=None

def backtrack():
    r:int = 1; # r is the tree level, index of X
    X:list = [] # [1:N];
    for i in range(N): 
        X[i] = a0 # endfor // initialize X
    while r > 0:
        getnext(X,r)
        # assigns to X[r] its next C-compliant value,
        # if available; else, it re-initlizes X[r] to 𝒂𝒂𝟎𝟎
        if (X[r] == a0):
            r = r-1 # backtrack to the previous level
        elif r == N:
            print(X); # a new complete solution
        else:
            r = r+1
        #endif
    # endwhile
# end backtrack

def getnext(X,r):
    X[r] = X[r] + 1; # next tentative value
    while (X[r] <= am):
        if (bound(X,r) == True):
            return; # new value for X[r] is found
        else: # try the next value in S
            X[r] = X[r] + 1
        # endif
    #endwhile
    # if getnext has not returned, that
    # means no C-compliant remaining
    # value was found. Re-initialize X[r]
    X[r] = a0
# end getnext

def bound(X,r):
    # X[1:r-1] have C-compliant values. Bound checks to see if X[r] is C-compliant.
    # next, check for violations that could be incurred by X[r]
    for i in range(r-1):
        if (is_edge(r,i)) and (X[r] == X[i]):
            return False
        # endif
    # endfor
    return True
# end Bound


# ------------------------------ #

def parse_input(input_str: str) -> dict[int, list[str]]:
    """parse input expression into variables"""
    expression = input_str.replace(" ", "")

    literal_pattern = r"(\w+'?)"  # r"(x_\d+'?)"
    clause_pattern = r"\([^()]+\)"

    clauses = re.findall(clause_pattern, expression)
    clauses = {clause: re.findall(literal_pattern, clause) for i, clause in enumerate(clauses)}
    return clauses

if __name__ == "__main__":
    cnf_test_expressions = [
        "(A)",  # 1. {'A':True}
        "(A')",  # 2. {'A':False}
        "(A)(A')",  # 3. None
        "(X+Y)",  # 4. {'X':True,'Y':*}
        "(X+Y')",  # 5. {'X':True,'Y':*}
        "(X'+Y)",  # 6. {'X':*,'Y':True}
        "(X'+Y')",  # 7. {'X':*,'Y':False}
        "(X+Y)(X'+Y)",  # 8. {'X':True,'Y':True}
        "(X+Y)(X'+Y')",  # 9. {'X':True,'Y':False}
        "(x_1' + x_2)(x_1' + x_3)",
        "(x_1' + x_2 + x_4') (x_2 + x_3' + x_4) (x_1 + x_2' + x_3) (x_1 + x_2 + x_3)",
        "(x_1' + x_2 + x_4' + x_5') (x_2 + x_3 + x_5' + x_6') (x_1 + x_2 + x_3 + x_5)",
    ]

    for cnf_expr in cnf_test_expressions:
        parse_result = parse_input(cnf_expr)
        print(f"expr: {cnf_expr}=1")
        print(f"parsed:\n{pformat(parse_result)}")
        print()



