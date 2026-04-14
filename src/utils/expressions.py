import logging
from pprint import pformat
from collections import namedtuple
from itertools import count, combinations
from typing import Tuple, Any


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
        return f"{self.title}"  # `A`
        # return f"{var_id}[{self.title}]"  # `V_0[A]`
        # return f"{var_id}[{self.title}={int(self.value)}]"  # `V_0[A=1]` # todo: use this one
        # return f"{var_id}::[{self.title}={int(self.value)}]"  # `V_0::[A=1]`
        # return f"{var_id}::{self.title}={int(self.value)}"   # `V_0::A=1`
        # return f"{var_id}::{self.title}[{int(self.value)}]"    # `V_0::A[1]`

    def __repr__(self):
        var_id = f"V_{self.id}" if INT_ID else f"{self.id}"
        return f"{var_id}[{self.title}]"  # `V_0[A]`
        # return f"{var_id}[{self.title}={int(self.value)}]"  # `V_0[A=1]` # todo: use this one?


class Literal(Variable):
    """
    A literal is an occurrence of a variable in either natural or complementary form
    eg. in `(x_1' + x_2)(x_1' + x_3)`
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

    def __init__(self, k: int, variables: list[Variable], form: str):
        assert form in [CNF_KEY, DNF_KEY]
        self.k = k
        self.variables = []
        self.form = form

        self.ingest(variables)

    def ingest(self, variables: list[Variable]):
        assert (isinstance(var, Variable) for var in variables)
        self.variables = list(variables)

    def __str__(self):
        form_terms = {
            CNF_KEY: "+",
            DNF_KEY: "*",
        }
        term = form_terms[self.form] if self.form else "?"  # default to 'unknown'
        return "(" + f" {term} ".join(self.str_list()) + ")"
        # return f" {term} ".join(objstr_list(self.variables))

    def str_list(self):
        return str_list(self.variables)


class Expression:
    def __init__(self, clauses: list[Clause], clause_form):
        self.clauses = clauses
        self.form = clause_form

    def __str__(self):
        return "".join(self.str_list())

    def str_list(self):
        """returns a string of all clauses"""
        return str_list(self.clauses)


# ------------------------------- #
#          Helper Funcs           #
# ------------------------------- #


def str_list(obj_list: list):
    """converts list of objects into a list of their strings"""
    return list(map(str, obj_list))


def obj_str(obj_list: list, indent=0):
    """converts list of objects into a formatted string"""
    pad = " " * indent
    delim = ", "
    sbracket, ebracket = "[", "]"
    if indent:
        delim = "\n"
        sbracket, ebracket = "[" + delim, delim + "]"
    return (
        sbracket
        + delim.join(f'{pad}"{objstr}"' for objstr in str_list(obj_list))
        + ebracket
    )


# -------------------------- #
#         local main         #
# -------------------------- #

if __name__ == "__main__":
    print("running `expressions.py`")
    print()
    # -------------------------- #
    #           tests            #
    # -------------------------- #

    tlogger = logging.getLogger("tests")
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    tlogger.addHandler(handler)
    tlogger.setLevel(logging.DEBUG)

    def seperator(pfunc):
        def wrapper():
            print()
            pfunc()
            print()

        return wrapper

    def bar(n=80):
        """returns a bar ('-') string of specified length n"""
        return "-" * n

    newline = "\n"
    bar40 = bar(40)
    bar80 = bar(80)

    def test_title(title_str: str, to_print: bool = True):
        if not to_print:
            return
        pad = 4
        n = len(title_str)
        title_bar = bar(n + 2 * pad)
        title_block = (
            f"#{title_bar}#",
            f"#{' '*pad}{title_str.title()}{' '*pad}#",
            f"#{title_bar}#",
        )
        return "\n".join(title_block)

    def test_variables(_, main_test: bool = True) -> Tuple[Any, list[str]]:
        VAR_DATA_KEY = "variable"
        TEST_PASSES_KEY = "test_passes"
        event_lines: list[str] = []  # hold strings regarding test events

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

        variables: list[Variable] = []
        event_lines.append("running tests:")
        for test_case in var_tests:
            var_data = test_case[VAR_DATA_KEY]
            should_pass = test_case[TEST_PASSES_KEY]

            tname = var_data[0]
            var = None
            test_str = ""
            try:
                var = Variable(*var_data)
                variables.append(var)
                test_str = f"Passes: created {var} :: (has value? {var.hasValue()})"

            except Exception as e:
                if not should_pass and isinstance(e, AssertionError):
                    test_str = f'Passes: assert caught on "Variable{var_data}"'
                else:
                    test_str = f'Fails: "Variable{var_data}" not created'

            if main_test:
                event_lines.append(f"  Test {tname:<2} {test_str}")

        event_lines.append(bar80)

        complements = [var.complement() for var in variables]
        complements_str = (
            f"generating complements to:"
            f"\n    {obj_str(variables)}"
            f"\n => {obj_str(complements)}"
        )

        event_lines.append(complements_str)
        event_lines.append(bar80)

        variables += complements
        return variables, event_lines

    def test_clauses(variables, main_test: bool = True) -> Tuple[Any, list[str]]:
        event_lines: list[str] = []  # hold strings regarding test events

        cnf_clauses = []
        # dnf_clauses = []
        var_combos: list[tuple] = []
        k_cutoff = 4  # 6  # stop combinations at `k = k_cutoff - 1`

        # combine variable terms for creating Clauses
        for k in range(2, k_cutoff):
            combos = list(combinations(variables, k))
            var_combos = [c for c in combos[:5] + combos[-5:]]

            if main_test:
                event_lines.append(f"generating {k}SAT clauses:")

            for clause_vars in var_combos:
                cnf_clause = Clause(len(clause_vars), clause_vars, CNF_KEY)
                # dnf_clause = Clause(len(clause_vars), clause_vars, DNF_KEY)

                cnf_clauses.append(cnf_clause)
                # dnf_clauses.append(dnf_clause)

                if main_test:
                    event_lines.append(f"  generated cnf_clause: {cnf_clause}")
                    # event_lines.append(f"  generated dnf_clause: {dnf_clause}")

        return cnf_clauses, event_lines

    def test_expressions(clauses, main_test: bool = True) -> Tuple[Any, list[str]]:
        event_lines: list[str] = []  # hold strings regarding test events

        all_expressions = []
        clause_combos: list[tuple] = []
        t_cutoff = 4  # stop term combinations at t = t_cutoff - 1

        # combine clause terms for creating Expressions
        for t in range(1, t_cutoff):
            combos = list(combinations(clauses, t))
            clause_combos = [c for c in combos[:5] + combos[-5:]]

            if main_test:
                event_lines.append(f"generating expressions of length {t}:")

            clause_list: list[Clause]
            for i, clause_list in enumerate(clause_combos):
                k = clause_list[0].k

                form = clause_list[0].form
                next_expression = Expression(clause_list, form)
                all_expressions.append(next_expression)

                if main_test:
                    event_lines.append(f"  generated {k}SAT expr: {next_expression}")

        return all_expressions, event_lines

    tests = {  # heirarchical tests (produce results used by next test in sequence)
        "Variable Test": test_variables,
        "Clause Test": test_clauses,
        "Expression Test": test_expressions,
    }

    result = None
    for ttitle, tfunc in tests.items():
        event_lines = []
        result, event_lines = tfunc(result)

        ttitle = test_title(ttitle, to_print=True)
        tresult = f"{tfunc.__name__ + '()'} result set:" f"\n{obj_str(result,indent=2)}"

        event_lines = [
            newline + ttitle,
            newline.join(event_lines),
            tresult,
            bar80,
            newline,
            newline,
        ]

        tlogger.info("\n".join(event_lines))
else:
    print("importing `expressions.py`")
