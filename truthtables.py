# Boolean Literals
from enum import Enum
from typing import Iterable,Collection

symbols = Enum('Symbols',[
    ('TRUE','1'),
    ('FALSE','0'),
    ('NOT','!'),
    ('AND',' ^ '),
    ('OR',' v '),
    ('XOR',' x '),
    ('THEN','-->'),
    ('IFF','<->'),
    ])

class Literal:
    def __init__(self,variable,value):
        self.variable = variable
        self.value = value
        self.str = ''

    def __str__(self):
        if not self.str:
            result = [symbols.NOT.value if not self.value else ' '] + [self.variable]
            self.str =  ''.join(result)
        return self.str



def print_table(variables,operations=['and','or','xor','xnor']):
    n = len(variables) #number of variables
    ops = len(operations)
    variable_values = {var:(0,1) for var in variables}

    def bin_combinations(variables,levels):
        values = (0,1)
        if levels == 0:
            return values
        lowervalues = bin_combinations(variables,levels-1)
        return [(v1,*v2) if isinstance(v2, Iterable) else (v1,v2) for v1 in values for v2 in lowervalues]

    
    rows = bin_combinations(variables,n-1)

    cols = []
    for var in variable_values.keys():
        col_title = f"{var}"
        cols.append((len(col_title),col_title))

    title_lens = [t[0] for t in cols]
    header = '|' + ' | '.join([t[1] for t in cols]) + ' |'
    bar = '-'*len(header)

    lines = [bar,header,bar]
    for vals in rows:
        row = [f"{v:{title_lens[i]}}" for i,v in enumerate(vals)]
        lines.append('|'+' | '.join(row)+' |')
    lines.append(bar)

    print('\n'.join(lines))







def test():
    print("test 1: create literals")
    var_1 = Literal('A',value=True)
    print(var_1)
    var_2 = Literal('A',value=False)
    print(var_2)

    print("test 2: print table")
    # given a variable, display all Truth values 
    print_table([var_1,var_2,Literal('B',value=True)])
    
    # given a pair of variables, display all Truth values (for  and/or/xor/xnor)

    # given a set of variables, display Truth values of all combinations (for  and/or/xor/xnor)


    return

if __name__ == "__main__":
    test()


