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

    def bin_combinations(variables,levels):
        values = (0,1)
        if levels == 0:
            return values
        return [(v1,*v2) if isinstance(v2, Iterable) else (v1,v2) for v1 in values for v2 in bin_combinations(variables,levels-1)]

    
    rows = bin_combinations(variables,n-1)

    col_widths = []
    cols = []
    for var in variables:
        col_title = f"{var}"
        col_widths.append(len(col_title))
        cols.append(col_title)

    header = '|' + ' | '.join(cols) + ' |'
    bar = '-'*len(header)

    lines = [bar,header,bar]
    for vals in rows:
        print(rows, vals)
        row = [f"{v:{col_widths[i]}}" for i,v in enumerate(vals)]
        lines.append('|'+' | '.join(row)+' |')
    lines.append(bar)

    print('\n'.join(lines))







def full_test():

    def test_literal(val,pos):
        try:
            var = Literal(val,pos)
        except Exception as e:
            print(e)
        return var
            
    def test_table(varlist):
        try:
            print_table(varlist)
        except Exception as e:
            print(e)
        print()



    print("test 1: create literals")
    var_1 = test_literal('A',True)
    var_2 = test_literal('A',False)
    print(var_1)
    print(var_2)
    print()

    print("test 2: print table")
    # given a variable, display all Truth values 
    test_table([var_1])
    test_table([var_1,var_2])
    test_table([var_1,var_2,Literal('B',value=True)])

    
    # given a pair of variables, display all Truth values (for  and/or/xor/xnor)

    # given a set of variables, display Truth values of all combinations (for  and/or/xor/xnor)


    return

if __name__ == "__main__":
    full_test()


