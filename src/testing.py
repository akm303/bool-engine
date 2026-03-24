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
    """check if actual result is expected result"""
    return expected == actual


def list_check(input: Any, potential: Collection, actual: Any) -> bool:
    """check if actual result in list of potential expected results"""
    return actual in potential


class TestCase:
    """an individual test case and its expected result"""

    test_counter = count()

    def __init__(self, input_value, expected, validator: Callable, label: str = ""):
        self.test_id = next(TestCase.test_counter)
        self.title = f"Test {self.test_id}"
        self.input = input_value
        self.expected = expected  # expected result/output
        self.validator = validator
        self.label = label if label else input_value

    def get_testcase(self):
        return {"input": self.input, "expected": self.expected, "check": self.validator}

    def call(self, solver: Callable):
        # ! issue with this; if input is supposed to be a single tuple rather than its internals
        if isinstance(self.input, tuple):
            return solver(*self.input)
        return solver(self.input)

    def check(self, actual) -> bool:
        check_result = passes(self.validator(self.input, self.expected, actual))
        dprint(
            f"checking:"
            + f"\ninput={self.input}"
            + f"\n  expect={self.expected}"
            + f"\n  actual={actual}"
            + f"\ncase: {check_result}"
        )
        dprint()
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

    def __init__(self, test_cases: Collection[TestCase], solver: Callable):
        self.test_cases = test_cases
        self.solver = solver
        self.results = {}

    def run_case(self, test_case: TestCase, i: int = 0) -> bool:
        test_actual = test_case.call(self.solver)
        test_result = test_case.check(test_actual)
        return test_result

    def run(self):
        self.results = {
            test_case: self.run_case(test_case, i)
            for i, test_case in enumerate(self.test_cases)
        }

    def get_results(self):
        return {test_case.title: result for test_case, result in self.results.items()}

    def all_passed(self):

        return len(self.results) > 0 and all(
            result == PASS
            for test_case, result in self.results.items()
            if test_case in self.test_cases
        )

    def get_passed(self):
        pass_list = [
            f"{test_case.title}: {test_case.input}"
            for test_case, test_result in self.results.items()
            if test_result == PASS
        ]
        # dprint(f"TestRunner:get_passed:passed: {pass_list}")
        return pass_list

    def get_failed(self):
        fail_list = [
            f"{test_case.title}: {test_case.input}"
            for test_case, test_result in self.results.items()
            if test_result == FAIL
        ]
        # dprint(f"TestRunner:get_passed:failed: {fail_list}")
        return fail_list

    def __str__(self):

        solver_name = self.solver.__name__

        all_passed = self.all_passed()
        passing_tests = self.get_passed()
        failing_tests = self.get_failed()

        rstring = (
            f"\nTesting {solver_name}():"
            + f"\ncases: {self.test_cases}"
            # + f"\nall passed? {all_passed}"
            + f"\npassing: {passing_tests}"
            # + f"\npassing: {pformat(passing_tests,compact=True,indent=6)}"
            + f"\nfailing: {failing_tests}"
            # + f"\nfailing: {pformat(failing_tests,compact=True,indent=6)}"
            + "\n"
        )

        # rstring += f"\n  test cases:" + f"\n    {self.test_cases}"
        return rstring


# ----------------------------------------- #
# ----------------------------------------- #

KEY_SOLVER = "solver"
KEY_CHECKER = "checker"
KEY_CASES = "cases"

cnf_2sat_collection = {
    KEY_SOLVER: run_2sat,
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
        "(A + A)(A' + A')": True,  # should fail
    },
}

cnf_ksat_collection = {
    KEY_SOLVER: run_ksat,
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


def setup_test(test_collection: dict):
    # unpack test elements
    solver = test_collection[KEY_SOLVER]
    validator = test_collection[KEY_CHECKER]
    test_cases = test_collection[KEY_CASES]

    # define test-cases and test objects
    test_cases = [
        TestCase(expr, result, validator) for expr, result in test_cases.items()
    ]
    tester = TestRunner(test_cases, solver)
    return tester


def print_test_collection(test_collection):
    print(f"test collection: {{")
    print(f"  solver: {test_collection[KEY_SOLVER].__name__}")
    print(f" checker: {test_collection[KEY_CHECKER].__name__}")
    print(f"   cases: {test_collection[KEY_CASES]}")
    print("}")


def tester_test():
    N = 3

    def run_sum(a, b):
        return a + b

    def tester_checker(tester: TestRunner, all_should_pass: True, n_should: dict):
        all_pass = tester.all_passed()
        n_passed = len(tester.get_passed())
        n_failed = len(tester.get_failed())

        n_should_pass = n_should["pass"]
        n_should_fail = n_should["fail"]

        if (all_pass and not all_should_pass) or (not all_pass and all_should_pass):
            print(
                f"Tester Failed (all_pass={all_pass} when expected_pass={all_should_pass})"
            )
            return False

        if n_failed != n_should_fail:
            print(f"Tester Failed ({n_failed} tests failed, expected {n_should_fail})")
            return False
        if n_passed != n_should_pass:
            print(f"Tester Failed ({n_passed} tests passed, expected {n_should_pass})")
            return False

        return True

    print()

    tester_collection = {
        KEY_SOLVER: run_sum,
        KEY_CHECKER: exact_check,
        KEY_CASES: {(a, b): a + b for b in range(N) for a in range(N)},
    }

    # # v3
    # number of tests that should pass/fail in the tester pre/post tester.run()
    tester_should_have = {
        "pre": {"pass": 0, "fail": 0},
        "post": {"pass": len(tester_collection[KEY_CASES]), "fail": 0},
    }

    print("Testing test script (base):")
    print_test_collection(tester_collection)

    # Testing sequence
    tester = setup_test(tester_collection)
    print(f"Pre Test Run: {tester}")
    tester_passed = tester_checker(
        tester, all_should_pass=False, n_should=tester_should_have["pre"]
    )
    if not tester_passed:
        print("TESTER TEST FAILED")
        return

    tester.run()
    print(f"Post Test Run: {tester}")

    tester_passed = tester_checker(
        tester, all_should_pass=True, n_should=tester_should_have["post"]
    )
    if not tester_passed:
        print("TESTER TEST FAILED")
        return

    print()
    print()
    tester_collection[KEY_CASES][(0, 0)] = 1  # force test to fail

    tester_should_have["post"]["fail"] += 1
    tester_should_have["post"]["pass"] -= 1
    print("Testing test script (1 failure):")
    print_test_collection(tester_collection)
    print()

    tester = setup_test(tester_collection)
    print(f"Pre Test Run: {tester}")
    tester_passed = tester_checker(
        tester, all_should_pass=False, n_should=tester_should_have["pre"]
    )
    if not tester_passed:
        print("TESTER TEST FAILED")
        return

    tester.run()
    print(f"Post Test Run: {tester}")

    tester_passed = tester_checker(
        tester, all_should_pass=False, n_should=tester_should_have["post"]
    )
    if not tester_passed:
        print("TESTER TEST FAILED")
        return

    print()
    print()
    tester_collection[KEY_CASES][(N - 1, N - 1)] = 0  # force test to fail second time
    tester_should_have["post"]["fail"] += 1
    tester_should_have["post"]["pass"] -= 1
    print("Testing test script (2 failures):")
    print_test_collection(tester_collection)
    print()
    # Testing sequence
    tester = setup_test(tester_collection)
    print(f"Pre Test Run: {tester}")
    tester_passed = tester_checker(
        tester, all_should_pass=False, n_should=tester_should_have["pre"]
    )
    if not tester_passed:
        print("TESTER TEST FAILED")
        return

    tester.run()
    print(f"Post Test Run: {tester}")
    tester_passed = tester_checker(
        tester, all_should_pass=False, n_should=tester_should_have["post"]
    )
    if not tester_passed:
        print("TESTER TEST FAILED")
        return
    print("Tester Passes")
    print()


def run_sat_tests():
    sat_tests = [cnf_2sat_collection, cnf_ksat_collection]
    for sat_test_collection in sat_tests:
        tester = setup_test(sat_test_collection)
        tester.run()

        # get results
        all_passed = tester.all_passed()
        output_msg = bar40 + "\n"
        output_msg += (
            "All Passed" if all_passed else f"Failed Tests:\n  {tester.get_failed()}"
        )
        print(output_msg)
        print()
        print(bar40)
        print(bar40)
        print()
        print()


def run_all_tests():
    util_tests = [tester_test, run_sat_tests]

    for test in util_tests:
        print(bar40)
        print(bar40)
        print(f"running: {test.__name__}()")
        test()
        print()
        print(f"completed: {test.__name__}()")
        print(bar40)
        print(bar40)
        print()
        print()


if __name__ == "__main__":
    args = parse_flags()
    set_debug(args.debug)
    run_all_tests()
