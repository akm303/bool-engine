from itertools import count

# -------------------------- #
#          Objects           #
# -------------------------- #


class Variable:
    id_counter = count()

    def __init__(self, title: str, value: bool):
        assert isinstance(title, str)
        assert isinstance(value, bool)
        self.id = next(Variable.id_counter)
        self.title = title
        self.val = value

    def hasValue(self):
        return self.val in [True, False]

    def __str__(self):
        return f"V_{self.id}::[{self.title}={int(self.val)}]"   # `V_0::[A=1]`
        # return f"V_{self.id}::{self.title}={int(self.val)}"   # `V_0::A=1`
        # return f"V_{self.id}::{self.title}[{int(self.val)}]"    # `V_0::A[1]`


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
def test_variable():
    VAR_DATA_KEY = "variable"
    TEST_PASSES_KEY = "test_passes"

    all_tests = [
        {VAR_DATA_KEY: ("A", True), TEST_PASSES_KEY: True},
        {VAR_DATA_KEY: ("B", False), TEST_PASSES_KEY: True},
        {VAR_DATA_KEY: ("C", 1), TEST_PASSES_KEY: False},
        {VAR_DATA_KEY: ("D", 0), TEST_PASSES_KEY: False},
        {VAR_DATA_KEY: ("E", None), TEST_PASSES_KEY: False},
        {VAR_DATA_KEY: (5, True), TEST_PASSES_KEY: False},
        {VAR_DATA_KEY: (5, 1), TEST_PASSES_KEY: False},
    ]

    variables = []
    for test_data in all_tests:
        var_data = test_data[VAR_DATA_KEY]
        should_pass = test_data[TEST_PASSES_KEY]
        
        test_name = var_data[0]
        var = None
        try:
            var = Variable(*var_data)
            print(f"{test_name} Passes: created {var}")
            varHasValue = var.hasValue()
            print(f"{test_name} Passes: {var} has value? {varHasValue}")

            variables.append(var)

        except Exception as e:
            if not should_pass and isinstance(e, AssertionError):
                print(f"{test_name} Passes: assertion caught on Variable{var_data}")
            else:
                print(f"{test_name} Fails: Variable{var_data} not created")
    return variables


if __name__ == "__main__":
    result = test_variable()
    print(list(map(str,result)))
    # test_literal()


# class CNFExpression(Expression):
