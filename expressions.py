from itertools import count

# -------------------------- #
#          Objects           #
# -------------------------- #

INT_ID = True

class Variable:
    id_counter = count()

    def __init__(self, title: str, value: bool):
        assert isinstance(title, str)
        assert isinstance(value, bool)
        if INT_ID:
            self.id = next(Variable.id_counter) #id is an int
        else:
            self.id = f"V_{next(Variable.id_counter)}" #id is a str
        self.title = title
        self.value = value

    def hasValue(self):
        return self.value in [True, False]

    def toDict(self):
        return {self.id:{self.title:self.value}}

    def __str__(self):
        var_id = f"V_{self.id}" if INT_ID else f"{self.id}"

        return f"{var_id}::[{self.title}={int(self.value)}]"   # `V_0::[A=1]`
        # return f"{var_id}::{self.title}={int(self.value)}"   # `V_0::A=1`
        # return f"{var_id}::{self.title}[{int(self.value)}]"    # `V_0::A[1]`



class Literal(Variable):
    """
    A literal is an occurrence of a variable in either natural or complementary form
    eg. in `(x_1'+x_2)(x_1'+x_3)`
        - first literal in this expression is x_1'
        - second literal in this expression is x_2'
    """

    def __init__(self, title, value):
        super().__init__(title, value)


# class Expression:
#     def __init__(self,form,expr_str):
#         self.form = form
#         self.expr_str = expr_str


# -------------------------- #
#           tests            #
# -------------------------- #
def bar():
    print('-'*40)


def test_variable():
    VAR_DATA_KEY = "variable"
    TEST_PASSES_KEY = "test_passes"

    # test order matters
    all_tests = [
        {VAR_DATA_KEY: ("A", True), TEST_PASSES_KEY: True}, # valid
        {VAR_DATA_KEY: ("B", False), TEST_PASSES_KEY: True},# valid
        {VAR_DATA_KEY: ("C", 1), TEST_PASSES_KEY: False},   # invalid because value must be a bool
        {VAR_DATA_KEY: ("D", 0), TEST_PASSES_KEY: False},   # invalid because value must be a bool
        {VAR_DATA_KEY: ("E", None), TEST_PASSES_KEY: False},# invalid because value must be a bool
        {VAR_DATA_KEY: (5, True), TEST_PASSES_KEY: False},  # invalid because variable title must be string
        {VAR_DATA_KEY: (6, 1), TEST_PASSES_KEY: False},     # invalid because variable title must be string
        {VAR_DATA_KEY: ("H", True), TEST_PASSES_KEY: True}, # valid (check id counter)
    ]

    variables = []
    for test_data in all_tests:
        var_data = test_data[VAR_DATA_KEY]
        should_pass = test_data[TEST_PASSES_KEY]
        
        test_name = var_data[0]
        var = None
        bar()
        try:
            var = Variable(*var_data)
            print(f"{test_name} Passes:")
            print(f"        : created {var}")
            print(f"        : {var} has value? {var.hasValue()}")

            variables.append(var)

        except Exception as e:
            if not should_pass and isinstance(e, AssertionError):
                print(f"{test_name} Passes: assertion caught on Variable{var_data}")
            else:
                print(f"{test_name} Fails: Variable{var_data} not created")

    bar()
    return variables


if __name__ == "__main__":
    result = test_variable()
    print(list(map(str,result)))
    # test_literal()


# class CNFExpression(Expression):
