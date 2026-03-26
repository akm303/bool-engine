"""
Goal: Define common testing format for testing scripts

Tester(tests, solver)
- for algorithms
- for helper functions/common utilities

tests = {test_input : (expected_output,)}
solver = {algorithm, }

"""

from typing import Collection, Tuple, Callable, Iterable, Any
from itertools import count
from pprint import pformat

from cnf_2sat import run as run_2sat
from cnf_ksat import run as run_ksat
from common import *

PASS = "Pass"
FAIL = "Fail"


def passes(result: bool) -> str:
    """returns string based on whether test passed or failed"""
    return PASS if result else FAIL


def exact_check(input: Any, expected: Any, actual: Any) -> bool:
    """validator: check if actual result is expected result"""
    MAX_STR_LEN = 120
    case_passed = expected == actual
    input_str = f'"{input}"'
    result_str = "Pass" if case_passed else "Fail"

    outstr = (
        f'  check {input_str:10}: expect("{expected}") == actual("{actual}")? '
        f"{result_str}"
    )
    if len(outstr) > MAX_STR_LEN:
        outstr = (
            f"checking: input={input_str} => {result_str}"
            + f"\n       >: expect={expected}"
            + f"\n       >: actual={actual}"
        )
    dprint(outstr)
    return case_passed


def list_check(input: Any, potential: Collection, actual: Any) -> bool:
    """validator: check if actual result in list of potential expected results"""
    case_passed = actual in potential
    input_str = f'"{input}"'
    dprint(
        f'  case {input_str:10}: actual("{actual}") in potential:{potential}? '
        f"{'Pass' if case_passed else 'Fail'}"
    )
    return case_passed


class TestCase:
    """an individual test case and its expected result"""

    test_counter = count()

    def __init__(self, input_value, expected, validator: Callable, label: str = ""):
        self.test_id = next(TestCase.test_counter)
        self.title = f"Test Case {self.test_id}"
        self.input = input_value
        self.expected = expected  # expected result/output
        self.validator = validator
        self.label = label if label else f"{self.title}: {input_value}"

    def get_testcase(self):
        return {"input": self.input, "expected": self.expected, "check": self.validator}

    def call(self, solver: Callable):
        """call solver on test inputs"""
        # #! issue with this; if input is supposed to be a single tuple rather than its internals
        # print(self.label)
        if isinstance(self.input, tuple):
            return solver(*self.input)
        return solver(self.input)

    def check(self, actual) -> bool:
        """check it actual test output value matches expected value"""
        check_result = passes(self.validator(self.input, self.expected, actual))

        # output v1
        # dprint(
        #     f"checking:"
        #     + f"\ninput={self.input}"
        #     + f"\n  expect={self.expected}"
        #     + f"\n  actual={actual}"
        #     + f"\ncase: {check_result}"
        # )

        # output v2
        # dprint(
        #     f"checking: input={self.input} => {check_result}"
        #     + f"\n       >: expect={self.expected}"
        #     + f"\n       >: actual={actual}"
        # )
        # dprint()

        # output v3 - in self.validator function themselves
        return check_result

    def __hash__(self):
        return hash(self.test_id)

    def __eq__(self, item):
        return isinstance(item, TestCase) and self.test_id == item.test_id

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"\n  {self.title} : {self.input} -> {self.expected}?"
        # return f"\n  {self.title} : {self.input} -> {self.expected}? (by {self.validator.__name__}())"


class TestRunner:
    """runs collection of tests"""

    def __init__(self, test_cases: Collection[TestCase], solver: Callable, label=""):
        self.test_cases = test_cases
        self.solver = solver
        self.results = {}
        self.label = label if label else f"Testing `{solver.__name__}()`:"

    def run_case(self, test_case: TestCase, i: int = 0) -> bool:
        """run a single test case"""
        test_actual = test_case.call(self.solver)
        test_result = test_case.check(test_actual)
        return test_result

    def run_all(self):
        """run all test cases"""
        self.results = {
            test_case: self.run_case(test_case, i)
            for i, test_case in enumerate(self.test_cases)
        }

    def get_results(self) -> dict[str, str]:
        """get results of test as mapping of {case : pass|fail}"""
        return {test_case.title: result for test_case, result in self.results.items()}

    def all_passed(self) -> bool:
        """return true if all test cases passed"""
        return len(self.results) > 0 and all(
            result == PASS
            for test_case, result in self.results.items()
            if test_case in self.test_cases
        )

    def get_passed(self) -> list[str]:
        """get list of passing tests"""
        pass_list = [
            f"{test_case.title}: {test_case.input}"
            for test_case, test_result in self.results.items()
            if test_result == PASS
        ]
        # dprint(f"TestRunner:get_passed:passed: {pass_list}")
        return pass_list

    def get_failed(self) -> list[str]:
        """get list of failing tests"""
        fail_list = [
            f"{test_case.title}: {test_case.input}"
            for test_case, test_result in self.results.items()
            if test_result == FAIL
        ]
        # dprint(f"TestRunner:get_passed:failed: {fail_list}")
        return fail_list

    def __str__(self):

        all_passed = self.all_passed()
        passing_tests = self.get_passed()
        failing_tests = self.get_failed()

        rstring = (
            f"{self.label}:"
            # f"\n{self.label}:"
            + f"\ncases: {self.test_cases}"
            + f"\nallpass? {all_passed}"
            + f"\npassing: {passing_tests}"
            # + f"\npassing: {pformat(passing_tests,compact=True,indent=6)}"
            + f"\nfailing: {failing_tests}"
            # + f"\nfailing: {pformat(failing_tests,compact=True,indent=6)}"
            # + "\n"
        )

        # rstring += f"\n  test cases:" + f"\n    {self.test_cases}"
        return rstring


# ----------------------------------------- #
# ----------------------------------------- #
# Collection keys
KEY_LABEL = "label"
KEY_FUNC = "function"
KEY_CHECKER = "checker"
KEY_CASES = "cases"


def print_test_collection(test_collection: dict):
    print(f"test collection: {{")
    print(f"   label: {test_collection[KEY_LABEL]}")
    print(f"  solver: {test_collection[KEY_FUNC].__name__}")
    print(f" checker: {test_collection[KEY_CHECKER].__name__}")
    print(f"   cases: {test_collection[KEY_CASES]}")
    print("}")


def setup_test(test_collection: dict) -> TestRunner:
    # unpack test elements
    test_label = test_collection.get(KEY_LABEL, "")
    solver = test_collection[KEY_FUNC]
    validator = test_collection[KEY_CHECKER]
    test_cases = test_collection[KEY_CASES]

    # define test-cases and test objects
    test_cases = [
        TestCase(expr, result, validator) for expr, result in test_cases.items()
    ]
    tester = TestRunner(test_cases, solver, test_label)
    return tester


# ----------------------------------------- #
# ----------------------------------------- #
# meta tests
def tester_test() -> bool:
    """
    Tests tester objects (TestRunner and TestCase) to verify correct operation
    returns true if all test variations pass
    """
    N = 3
    PRE = "pre"
    POST = "post"

    # helpers to test tester itself
    def run_sum(a, b):
        """sum two number"""
        return a + b

    def test_runner_check_passed(
        tester: TestRunner, all_should_pass: bool, n_should_be_from: dict, title=""
    ):
        """verify expected state of tester object during test"""
        # aliasing & formatting
        all_should = all_should_pass  # alias for code formatter (black fmt)
        title = f" ({title.title()} Tester) " if title else title

        all_pass = tester.all_passed()
        if (all_pass and not all_should) or (not all_pass and all_should):
            print(f">{title}Failed: (all_pass={all_pass} when expected {all_should})")
            return False

        n_pass = len(tester.get_passed())
        n_fail = len(tester.get_failed())
        n_should_pass = n_should_be_from[PASS]
        n_should_fail = n_should_be_from[FAIL]
        if n_fail != n_should_fail:
            print(f">{title}Failed: ({n_fail} tests failed, expected {n_should_fail})")
            return False
        if n_pass != n_should_pass:
            print(f">{title}Failed: ({n_pass} tests passed, expected {n_should_pass})")
            return False

        print(f">{title}Passed\n")
        return True

    def update_expected_dict(
        base_dict: dict[str, dict[str, int]], delta_dict: dict[str, dict[str, int]]
    ) -> dict:
        """update values of expected results"""
        expected_dict = base_dict.copy()
        for prepost, valuedict in delta_dict.items():
            for passfail, value_update in valuedict.items():
                expected_dict[prepost][passfail] += value_update
        return expected_dict

    # setup test data
    # define base test collection
    tester_collection = {
        KEY_FUNC: run_sum,
        KEY_CHECKER: exact_check,
        KEY_CASES: {(a, b): a + b for b in range(N) for a in range(N)},
    }

    # define expected number of pass/fails expected before and after a test runs
    expect_base = {
        PRE: {PASS: 0, FAIL: 0},
        POST: {PASS: len(tester_collection[KEY_CASES]), FAIL: 0},
    }

    # define iterative adjustments where a test collection's case is modified
    # - key: one of the cases of the test collection
    # - value: tuple(
    #       an update to the result of that case
    #       an update to the expected pass/fails before/after a test runs
    # )
    #
    # the purpose is to inject changes to force tester to handle test collections
    # that would fail to verify correct operation

    test_updates = {
        None: None,
        (0, 0): [
            1,
            {
                PRE: {PASS: 0, FAIL: 0},
                POST: {PASS: -1, FAIL: 1},
            },
        ],
        (N - 1, N - 1): [
            0,
            {
                PRE: {PASS: 0, FAIL: 0},
                POST: {PASS: -1, FAIL: 1},
            },
        ],
    }

    # Testing sequence
    print(bar40)
    print("TESTER TEST (META)")
    print(bar40)

    expected = expect_base
    all_pass = True
    i = 0
    for case, update in test_updates.items():
        dprint(f"case: {case} | update: {update}")
        if case:
            new_result, expect_delta = update
            dprint(f"new_result for case={case}: {new_result}")
            dprint(f"expect_delta: {expect_delta}")
            tester_collection[KEY_CASES][case] = new_result
            expected = update_expected_dict(expected, expect_delta)

        # setup test
        tester_collection[KEY_LABEL] = f"TESTER RUN {i}"
        print(f"generating test from collection:")
        print_test_collection(tester_collection)
        print()

        tester = setup_test(tester_collection)
        print(f"test is set up: {tester}")

        # check tester before running - should always have none passing, none failing
        if not test_runner_check_passed(
            tester,
            all_should_pass=False,
            n_should_be_from=expected[PRE],
            title="pre run",
        ):
            # print("TESTER CHECK FAILED; after setup")
            return False

        # test is run
        print(f"test running...")
        tester.run_all()
        print()

        # check tester after running - passing/failing based on update; after first loop, should not 'all pass'
        print(f"test ran: {tester}")
        if not test_runner_check_passed(
            tester,
            all_should_pass=all_pass,
            n_should_be_from=expected[POST],
            title="post run",
        ):
            # print("TESTER CHECK FAILED; after run")
            return False

        # after first run, cases are updated so as to complete run but no longer fully pass
        all_pass = False
        print(bar40)
        print()

    return "Tester Passes"


# ----------------------------------------- #
# ----------------------------------------- #
# util tests


def check_fmt_case(original, expected, actual):
    case_passed = expected == actual
    original = f'"{original}"'
    print(
        f'  case {original:10}: expect("{expected}") == actual("{actual}")? '
        f"{'Pass' if case_passed else 'Fail'}"
    )
    return case_passed


# - syntax formatting to local
def test_syntax():
    def to_local_test():
        local_syntax_tests = {
            # and-based cases
            r"a&a": "a.a",
            r"a&&b": "a.b",
            r"a.c": "a.c",
            r"a\land d": "a.d",
            r"a\lande": "a.e",
            # or-based cases
            r"a|a": "a+a",
            r"a||b": "a+b",
            r"a+c": "a+c",
            r"a\lor d": "a+d",
            r"a\lore": "a+e",
        }

        total_results = []
        for test_case, test_expected in local_syntax_tests.items():
            test_actual = to_local(test_case)
            case_passed = check_fmt_case(test_case, test_expected, test_actual)
            total_results.append(case_passed)
        return total_results

    def from_local_test():
        syntax_tests = {
            "latex": {
                # and-based cases
                r"a&a": r"a\land a",
                r"a&&b": r"a\land b",
                r"a.c": r"a\land c",
                r"a\land d": r"a\land d",
                r"a\lande": r"a\land e",
                # or-based cases
                r"a|a": r"a\lor a",
                r"a||b": r"a\lor b",
                r"a+c": r"a\lor c",
                r"a\lor d": r"a\lor d",
                r"a\lore": r"a\lor e",
            },
            "code": {
                # and-based cases
                r"a&a": "a&a",
                r"a&&b": "a&b",
                r"a.c": "a&c",
                r"a\land d": "a&d",
                r"a\lande": "a&e",
                # or-based cases
                r"a|a": "a|a",
                r"a||b": "a|b",
                r"a+c": "a|c",
                r"a\lor d": "a|d",
                r"a\lore": "a|e",
            },
        }

        test_funcs = {
            "latex": to_LaTeX,
            "code": to_code,
        }

        total_results = []
        for test_lang, test_cases in syntax_tests.items():
            if test_lang == "code":
                for i, lang in enumerate(["py", "c"]):
                    print(f"testing for conversion to {test_lang}::{lang}")
                    for test_case, test_expected in test_cases.items():
                        test_expected = test_expected.replace("&", "&" * (i + 1))
                        test_expected = test_expected.replace("|", "|" * (i + 1))
                        test_actual = test_funcs[test_lang](test_case, lang)
                        case_passed = check_fmt_case(
                            test_case, test_expected, test_actual
                        )
                        total_results.append(case_passed)
                        # total_results.append((test_case,test_expected,test_actual,case_passed))
            else:
                print(f"testing for conversion to {test_lang}")
                for test_case, test_expected in test_cases.items():
                    test_actual = test_funcs[test_lang](test_case)
                    case_passed = check_fmt_case(test_case, test_expected, test_actual)
                    total_results.append(case_passed)
        return total_results

    print("Running Tests:")
    total_results = []
    total_results += to_local_test()
    total_results += from_local_test()

    final_result = all(r == True for r in total_results)
    print(f"\nAll test cases passed? {final_result}")
    return total_results


# ----------------------------------------- #
# ----------------------------------------- #
# src tests


cnf_2sat_collection = {
    KEY_LABEL: "2SAT Solver",
    KEY_FUNC: run_2sat,
    KEY_CHECKER: exact_check,
    KEY_CASES: {
        # custom examples
        "(X+Y)": True,
        "(X+Y')": True,
        "(X'+Y)": True,
        "(X'+Y')": True,
        "(X+Y)(X'+Y)": True,
        "(X+Y)(X'+Y')": True,
        "(x_1' + x_2)(x_1' + x_3)": True,
        # example from 2SAT on website
        "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1')": True,
        "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1') (x_3' + x_1)": False,
        "(x_2' + x_1) (x_1' + x_3) (x_3 + x_1) (x_3' + x_2') (x_3' + x_2)": False,  # swapped x_1 & x_2
        "(x_3' + x_2) (x_2' + x_1) (x_1 + x_2) (x_1' + x_3') (x_1' + x_3)": False,  # swapped x_1 & x_3
        # custom examples
        "(x_a' + x_a)": True,
        "(A + A)(A' + A')": False,
        # "(A + A)(A' + A')": True,  # should fail
    },
}

cnf_ksat_collection = {
    KEY_LABEL: "kSAT Solver",
    KEY_FUNC: run_ksat,
    KEY_CHECKER: exact_check,
    KEY_CASES: {
        # custom examples
        "(A)": (True, {"A": 1}),
        "(A')": (True, {"A": 0}),
        "(A)(A')": (False, None),
        "(X+Y)": (True, {"X": 1, "Y": "*"}),
        "(X+Y')": (True, {"X": 1, "Y": "*"}),
        "(X'+Y)": (True, {"X": 1, "Y": 1}),
        "(X'+Y')": (True, {"X": 1, "Y": 0}),
        "(X+Y)(X'+Y)": (True, {"X": 1, "Y": 1}),
        "(X+Y)(X'+Y')": (True, {"X": 1, "Y": 0}),
        "(x_1' + x_2)(x_1' + x_3)": (True, {"x_1": 1, "x_2": 1, "x_3": 1}),
        "(x_1' + x_2 + x_4') (x_2 + x_3' + x_4) (x_1 + x_2' + x_3) (x_1 + x_2 + x_3)": (
            True,
            {
                "x_1": 1,
                "x_2": 1,
                "x_3": "*",
                "x_4": "*",
            },
        ),
        "(x_1' + x_2' + x_4' + x_5') (x_2' + x_3 + x_5' + x_6') (x_1 + x_2 + x_3 + x_5)": (
            True,
            {
                "x_1": 1,
                "x_2": 1,
                "x_3": 1,
                "x_4": 1,
                "x_5": 0,
                "x_6": "*",
            },
        ),
        # # example form 2SAT on website
        # "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1')":
        # "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1') (x_3' + x_1)",
        # "(x_2' + x_1) (x_1' + x_3) (x_3 + x_1) (x_3' + x_2') (x_3' + x_2)":
        # "(x_a' + x_1) (x_1' + x_3) (x_3 + x_1) (x_3' + x_a') (x_3' + x_a)":
        # # custom examples
        # "(x_a' + x_a)":
        # "(A + A)(A' + A')":
    },
}
sat_tests = [cnf_2sat_collection, cnf_ksat_collection]


def run_test(test):
    test_title = "Test: ???"
    test_hook = None
    all_passed_hook = None

    if isinstance(test, dict):
        tester = setup_test(test)

        test_title = tester.label
        test_hook = tester.run_all
        all_passed_hook = tester.all_passed

    # elif isinstance(test,):
    else:  # is function
        test_title = f"`{test.__name__}()`"
        test_hook = test

    print(f"## running: {test_title}")

    print(bar40)
    print("```tex")

    results = test_hook()

    output_msg = "\n >>> "
    # output_msg = "\n" + bar40 + "\n"
    if all_passed_hook:
        all_passed = all_passed_hook()
        output_msg += (
            "All Passed" if all_passed else f"Failed Tests:\n  {tester.get_failed()}"
        )
    else:
        output_msg += f"{results}"

    output_msg += "\n" + bar40 + "\n"

    print()
    print()
    print(bar40)
    print(f"{test_title} output: {output_msg}")
    print()

    print("```")
    print(bar40)
    print(f"## completed: {test_title}")
    print()
    print()



if __name__ == "__main__":
    args = parse_flags()
    set_debug(args.debug)

    # array of test functions (callable) or collections (dict) to be ran
    # if function, runs test directly
    # if collection, sets up and runs test
    all_tests = [tester_test] + sat_tests
    for test in all_tests:
        run_test(test)
