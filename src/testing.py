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

    def __init__(
        self, test_id, input_value, expected, validator: Callable, label: str = ""
    ):
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
        return passes(self.validator(self.input, self.expected, actual))

    def __hash__(self):
        return hash(self.test_id)

    def __eq__(self, item):
        return isinstance(item, TestCase) and self.test_id == item.test_id

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"\n{self.title} : {self.input} -> {self.expected} ({self.validator.__name__})?"


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

    # def run_case(self, test_case: TestCase, i: int = 0) -> bool:
    #     test_actual = self.solver(test_case.input, i)
    #     test_result = test_case.check(test_actual)
    #     return test_result

    def run(self):
        self.results = {
            test_case: self.run_case(test_case, i)
            for i, test_case in enumerate(self.test_cases)
        }

    def get_results(self):
        return {test_case.title: result for test_case, result in self.results.items()}

    def all_passed(self):
        return all(result == PASS for result in self.results.values())

    def get_passed(self):
        pass_list = [
            f"{test_case.title}: {test_case.input}"
            for test_case, test_result in self.results.items()
            if test_result == PASS
        ]
        dprint(f"passed: {pass_list}")
        return pass_list

    def get_failed(self):
        fail_list = [
            f"{test_case.title}: {test_case.input}"
            for test_case, test_result in self.results.items()
            if test_result == FAIL
        ]
        dprint(f"failed: {fail_list}")
        return fail_list

    def __str__(self):
        all_passed = self.all_passed()
        passing_tests = self.get_passed()
        failing_tests = self.get_failed()

        rstring = (
            f"\n  all passed? {all_passed}"
            + f"\n    passing:"
            + f"\n    {pformat(passing_tests,compact=True,indent=6)}"
            + f"\n    failing:"
            + f"\n    {pformat(failing_tests,compact=True,indent=6)}"
        )

        # rstring += f"\n  test cases:" + f"\n    {self.test_cases}"
        return rstring


cnf_2sat_cases = {
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
}

cnf_tests = [
    # custom examples
    "(A)",  # 1. {'A':1}
    "(A')",  # 2. {'A':0}
    "(A)(A')",  # 3. None
    "(X+Y)",  # 4. {'X':1,'Y':*}
    "(X+Y')",  # 5. {'X':1,'Y':*}
    "(X'+Y)",  # 6. {'X':1,'Y':1}
    "(X'+Y')",  # 7. {'X':1,'Y':0}
    "(X+Y)(X'+Y)",  # 8. {'X':1,'Y':1}
    "(X+Y)(X'+Y')",  # 9. {'X':1,'Y':0}
    "(x_1' + x_2)(x_1' + x_3)",  # 10. {'x_1':1, 'x_2':1, 'x_3':1}
    "(x_1' + x_2 + x_4') (x_2 + x_3' + x_4) (x_1 + x_2' + x_3) (x_1 + x_2 + x_3)",  # 11. {'x_1':1, 'x_2':1, 'x_3':*, 'x_4':*}
    "(x_1' + x_2' + x_4' + x_5') (x_2' + x_3 + x_5' + x_6') (x_1 + x_2 + x_3 + x_5)",  # 12. {'x_1':1, 'x_2':1, 'x_3':*, 'x_4':*}
    # example form 2SAT on website
    "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1')",
    "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1') (x_3' + x_1)",
    "(x_2' + x_1) (x_1' + x_3) (x_3 + x_1) (x_3' + x_2') (x_3' + x_2)",  # swapped x_1 & x_2
    "(x_a' + x_1) (x_1' + x_3) (x_3 + x_1) (x_3' + x_a') (x_3' + x_a)",  # swapped x_1 & x_3
    # custom examples
    "(x_a' + x_a)",
    "(A + A)(A' + A')",
]


def tester_test():
    def run_sum(a, b):
        return a + b

    inputs = [(a, b) for b in range(10) for a in range(10)]
    test_results = {(a, b): a + b for a, b in inputs}
    sum_test = {
        TestCase("", test_input, result, exact_check)
        for test_input, result in test_results.items()
    }

    tester = TestRunner(sum_test, run_sum)
    print(f"Pre Run: tester: {tester}")

    tester.run()
    print("Running Test...")

    print(f"Post Run: tester: {tester}")


sat_funcs = [
    run_2sat,
    run_ksat,
]

def run_tests():
    print(bar40)
    test_id = (i for i in range(len(cnf_2sat_cases)))
    tests_2sat = [
        TestCase(next(test_id), expr, result, exact_check)
        for expr, result in cnf_2sat_cases.items()
    ]
    tester = TestRunner(tests_2sat, run_2sat)
    tester.run()
    all_passed = tester.all_passed()
    output_msg = bar40 + "\n"
    output_msg += (
        "All Passed" if all_passed else f"Failed Tests:\n  {tester.get_failed()}"
    )
    print(output_msg)



def all_tests():
    print(bar40)
    test_tester()
    print(bar40)
    print()

if __name__ == "__main__":
    args = parse_flags()
    set_debug(args.debug)
    run_tests()
