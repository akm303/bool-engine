from itertools import count

# -------------------------- #
#          Objects           #
# -------------------------- #

INT_ID = True
CNF_KEY = "CNF"
DNF_KEY = "DNF"


class Variable:
    id_counter = count()

    def __init__(self, title: str, value: bool):
        assert isinstance(title, str)
        assert isinstance(value, bool)
        if INT_ID:
            self.id = next(Variable.id_counter)  # id is an int
        else:
            self.id = f"V_{next(Variable.id_counter)}"  # id is a str
        self.title = title
        self.value = value

    def hasValue(self):
        return self.value in [True, False]

    def toDict(self):
        return {self.id: {self.title: self.value}}

    def complement(self):
        complement_title = (
            f"{self.title}'" if "'" not in self.title else self.title[:-1]
        )
        return Variable(f"{complement_title}", not self.value)

    def __str__(self):
        var_id = f"V_{self.id}" if INT_ID else f"{self.id}"

        return f"{var_id}[{self.title}={int(self.value)}]"  # `V_0[A=1]`
        # return f"{var_id}::[{self.title}={int(self.value)}]"  # `V_0::[A=1]`
        # return f"{var_id}::{self.title}={int(self.value)}"   # `V_0::A=1`
        # return f"{var_id}::{self.title}[{int(self.value)}]"    # `V_0::A[1]`


class Literal(Variable):
    """
    A literal is an occurrence of a variable in either natural or complementary form
    eg. in `(x_1'+x_2)(x_1'+x_3)`
        - first literal in this expression is `x_1`'
        - second literal in this expression is `x_2`'
    """

    def __init__(self, title, value):
        super().__init__(title, value)


class Clause:
    """
    A k-Clause is limited to at most k literals
    eg. 3SAT: `(x_1' + x_2 + x_4') (x_2 + x_3' + x_4) (x_1 + x_2' + x_3) (x_1 + x_2 + x_3) = T`
        clauses each have 3 literals:
            - "(x_1' + x_2 + x_4')"
            - "(x_2 + x_3' + x_4)"
            - "(x_1 + x_2' + x_3)"
            - "(x_1 + x_2 + x_3)"
    eg. 4SAT: `(x_1' + x_2 + x_4' + x_5') (x_2 + x_3 + x_5' + x_6') (x_1 + x_2 + x_3 + x_5)= T`
        clauses each have 4 literals:
            - "(x_1' + x_2 + x_4' + x_5')"
            - "(x_2 + x_3 + x_5' + x_6')"
            - "(x_1 + x_2 + x_3 + x_5)"
    """

    def __init__(self, k: int, variables: list, form: str):
        assert form in [CNF_KEY, DNF_KEY]
        self.k = k
        self.variables = []
        self.form = form

        self.ingest(variables)

    def ingest(self, variables):
        assert (isinstance(var, Variable) for var in variables)
        self.variables = list(variables)

    def __str__(self):
        term = " + " if self.form == CNF_KEY else " "
        return term.join(objstr_list(self.variables))


# class Expression:
#     def __init__(self,form,expr_str):
#         self.form = form
#         self.expr_str = expr_str


# -------------------------- #
#           tests            #
# -------------------------- #
def bar():
    print("-" * 40)


def objstr_list(var_list: list):
    # return f"[{', '.join(map(str, var_list))}]"
    return list(map(str, var_list))


def test_variable():
    VAR_DATA_KEY = "variable"
    TEST_PASSES_KEY = "test_passes"

    # test order matters
    var_tests = [
        {VAR_DATA_KEY: ("A", True), TEST_PASSES_KEY: True},  # valid
        {VAR_DATA_KEY: ("B", False), TEST_PASSES_KEY: True},  # valid
        {
            VAR_DATA_KEY: ("C", 1),
            TEST_PASSES_KEY: False,
        },  # invalid because value must be a bool
        {
            VAR_DATA_KEY: ("D", 0),
            TEST_PASSES_KEY: False,
        },  # invalid because value must be a bool
        {
            VAR_DATA_KEY: ("E", None),
            TEST_PASSES_KEY: False,
        },  # invalid because value must be a bool
        {
            VAR_DATA_KEY: (5, True),
            TEST_PASSES_KEY: False,
        },  # invalid because variable title must be string
        {
            VAR_DATA_KEY: (6, 1),
            TEST_PASSES_KEY: False,
        },  # invalid because variable title must be string
        {VAR_DATA_KEY: ("H", True), TEST_PASSES_KEY: True},  # valid (check id counter)
        {VAR_DATA_KEY: ("I'", True), TEST_PASSES_KEY: True},  # valid
        {VAR_DATA_KEY: ("J'", False), TEST_PASSES_KEY: True},  # valid
    ]

    variables = []
    for test_data in var_tests:
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

    complements = []
    var: Variable
    for var in variables:
        complements.append(var.complement())
    print(
        f"complements to:\n    {objstr_list(variables)}\n => {objstr_list(complements)}"
    )
    variables += complements

    return variables


def test_clause(variables):
    print(f"testing clauses on {objstr_list(variables)}")
    # vardict = {i: var for i, var in enumerate(variables)}
    clauses = []

    clausevars = variables[:3]
    # vardict[0],vardict[1],vardict[2]
    c1 = Clause(3, clausevars, CNF_KEY)
    print(c1)
    clauses.append(c1)

    return clauses


if __name__ == "__main__":

    def testtitle(test_title):
        pad = 4
        n = len(test_title)
        title_bar = "-" * (n + 2 * pad)
        print(f"#{title_bar}#")
        print(f"#" + " " * pad + f"{test_title.title()}" + " " * pad + "#")
        # print(f"#  {test_title.title()}  #")
        print(f"#{title_bar}#")

    def testsep():
        n = 3  # number of bars to print between tests
        print()
        for _ in range(n):
            bar()
        print()

    # tests = {
    #     'variable test':test_variable,
    #     'clause test':test_clause
    # }

    print()
    testtitle("variable test")
    result = test_variable()
    print(f"result of test_variable(): {objstr_list(result)}")
    # test_literal()
    testsep()

    print()
    testtitle("clause test")
    result = test_clause(result)
    print(f"result of test_clause(): {objstr_list(result)}")
    print(result)
    testsep()

    print()

# class CNFExpression(Expression):
