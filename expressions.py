from pprint import pformat
from collections import namedtuple
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


if __name__ == "__main__":

    def bar(to_print=True):
        if not to_print:
            return
        print("-" * 80)

    def testtitle(test_title, to_print=True):
        if not to_print:
            return
        pad = 4
        n = len(test_title)
        title_bar = "-" * (n + 2 * pad)
        title_str = (
            f"#{title_bar}#"
            + f"\n#"
            + " " * pad
            + f"{test_title.title()}"
            + " " * pad
            + "#"
            + f"\n#{title_bar}#"
        )
        print(title_str)

    def testsep(bars=2, to_print=True):
        if not to_print:
            return
        print()
        for _ in range(bars):
            bar()
        print()

    def objstr_list(var_list: list):
        # return f"[{', '.join(map(str, var_list))}]"
        return list(map(str, var_list))

    def obj_str(var_list: list, indent=0):
        # return f"[ {', '.join(objstr_list(var_list))} ]"
        # return pformat(objstr_list(var_list),indent=indent)
        pad = " " * indent
        delim = ", "
        sbracket, ebracket = "[", "]"
        if indent:
            delim = "\n"
            sbracket, ebracket = "[" + delim, delim + "]"
        return (
            sbracket
            + delim.join(f'{pad}"{objstr}"' for objstr in objstr_list(var_list))
            + ebracket
        )

    def test_variable(_, main_test: bool = True):
        VAR_DATA_KEY = "variable"
        TEST_PASSES_KEY = "test_passes"
        testtitle("variable test", main_test)

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
            {
                VAR_DATA_KEY: ("H", True),
                TEST_PASSES_KEY: True,
            },  # valid (check id counter)
            {VAR_DATA_KEY: ("I'", True), TEST_PASSES_KEY: True},  # valid
            {VAR_DATA_KEY: ("J'", False), TEST_PASSES_KEY: True},  # valid
        ]

        variables = []
        for test_data in var_tests:
            var_data = test_data[VAR_DATA_KEY]
            should_pass = test_data[TEST_PASSES_KEY]

            test_name = var_data[0]
            var = None
            # bar()
            test_str = ""
            try:
                var = Variable(*var_data)
                test_str = (
                    f"{test_name} Passes:"
                    + f"\n        : created {var}"
                    + f"\n        : {var} has value? {var.hasValue()}"
                )
                variables.append(var)

            except Exception as e:
                if not should_pass and isinstance(e, AssertionError):
                    test_str = (
                        f'{test_name} Passes: assertion caught on "Variable{var_data}"'
                    )
                else:
                    test_str = f'{test_name} Fails: "Variable{var_data}" not created'

            if main_test:
                print(test_str)
        bar()


        complements = []
        var: Variable
        for var in variables:
            complements.append(var.complement())
        print(
            f"complements to:" \
            +f"\n    {obj_str(variables)}" \
            +f"\n => {obj_str(complements)}"
        )
        variables += complements

        return variables

    def test_clause(variables, main_test: bool = True):
        testtitle("clause test", main_test)
        if main_test:
            print(f"testing clauses on {objstr_list(variables)}")
        clauses = []

        clausevars = variables[:3]
        c1 = Clause(3, clausevars, CNF_KEY)
        print(c1)
        clauses.append(c1)
        return clauses

    test_run = namedtuple("test_data", ["ttitle", "ftitle", "f"])

    tests = [
        test_run("Variable Test", "test_variable()", test_variable),
        test_run("Clause Test", "test_clause()", test_clause),
    ]

    result = None
    for ttuple in tests:
        print()
        tfunc = ttuple.f
        ttitle = ttuple.ttitle
        ftitle = ttuple.f.__name__ + "()"

        result = tfunc(result)
        print(f"\nresult of {ftitle}:\n{obj_str(result,indent=2)}")
        testsep()

    # tests = {
    #     'test_variable()':test_variable,
    #     'test_clause()':test_clause
    # }

    # result = None
    # for ttitle,tfunc in tests.items():
    #     print()
    #     result = tfunc(result)
    #     print(f"result of {ttitle}:\n{obj_str(result)}")
    #     testsep()

    # print()
    # result = test_variable()
    # print(f"result of test_variable():\n{obj_str(result)}")
    # testsep()

    # print()
    # result = test_clause(result)
    # print(f"result of test_clause():\n{obj_str(result)}")
    # testsep()

    print()
