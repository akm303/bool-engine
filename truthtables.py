# Boolean Literals
from enum import Enum

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

    def __str__(self):
        result = []
        if not self.value:
            result.append(symbols.NOT.value)
        result.append(self.variable)
        return ''.join(result)







def test():
    var_1 = Literal('A',value=True)
    print(var_1)
    var_2 = Literal('A',value=False)
    print(var_2)
    return

if __name__ == "__main__":
    test()


