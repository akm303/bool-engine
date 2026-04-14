from typing import Any, Collection, Callable
from itertools import count
from common import dprint, COMPACT

PASS = "Pass"
FAIL = "Fail"


# print = print_to_file(dprint, "tests/tester.tex")
# dprint = print_to_file(dprint, "debug/tester.tex")


def passes(result: bool) -> str:
    """returns string based on whether test passed or failed"""
    return PASS if result else FAIL


def check_exact(input: Any, expected: Any, actual: Any) -> bool:
    """validator: check if actual result is expected result"""
    MAX_STR_LEN = 100
    case_passed = expected == actual
    result_str = passes(case_passed)

    input_str = f'"{input}"'
    outstr = f"  {input_str} => {actual}: {result_str}"
    if not COMPACT:
        outstr = (
            f'  from {input_str:10} => expect("{expected}") ?? actual("{actual}")  '
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


def check_from_list(input: Any, potential: Collection, actual: Any) -> bool:
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
        if COMPACT:
            return self.title
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
        # print('.')
        test_result = test_case.check(test_actual)
        return test_result

    def run_all(self):
        """run all test cases"""
        print(f"Running {self.label}")
        self.results = {
            test_case: self.run_case(test_case, i)
            for i, test_case in enumerate(self.test_cases)
        }
        return self.all_passed()

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
KEY_VARIANTS = "variants"
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
