"""
Goal: Define common testing format for testing scripts

Tester(tests, solver)
- for algorithms
- for helper functions/common utilities

tests = {test_input : (expected_output,)}
solver = {algorithm, }

"""

from typing import Collection, Tuple, Callable, Iterable, Any

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

    def __init__(
        self, test_id, input_value, expected, validator: Callable, label: str = ""
    ):
        self.test_id = test_id
        self.title = f"Test {test_id}"
        self.input = input_value
        self.expected = expected  # expected result/output
        self.validator = validator
        self.label = label if label else input_value

    def get_testcase(self):
        return {"input": self.input, "expected": self.expected, "check": self.validator}

    def check(self, actual) -> bool:
        return passes(self.validator(self.input, self.expected, actual))
    


class TestRunner:
    """runs collection of tests"""

    def __init__(self, test_cases: Collection[TestCase], solver: Callable):
        self.test_cases = test_cases
        self.solver = solver
        self.results = {}

    def run_case(self, test_case: TestCase, i: int = 0) -> bool:
        test_actual = self.solver(test_case.input, i)
        test_result = test_case.check(test_actual)
        return test_result

    def run(self):
        self.results = {
            test_case.title: self.run_case(test_case, i)
            for i, test_case in enumerate(self.test_cases)
        }

    def get_results(self):
        return self.results

    def all_passed(self):
        return all(result == PASS for result in self.results.values())

    def get_passed(self):
        pass_list =  [
            test_id
            for test_id, test_result in self.results.items()
            if test_result == PASS
        ]
        dprint(f"passed: {pass_list}")
        return pass_list

    def get_failed(self):
        fail_list = [
            test_id
            for test_id, test_result in self.results.items()
            if test_result == FAIL
        ]
        dprint(f"failed: {fail_list}")
        return fail_list


cnf_2sat_tests = {
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
    "(A + A)(A' + A')": True, # should fail
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


def test_tester():
    def ab_sum(a,b):
        return a+b
    
    inputs = [(a,b) for b in range(10) for a in range(10)]
    test_results = {(a,b):a+b for a,b in inputs}

    tester = TestRunner()

def run_tests():
    test_id = (i for i in range(len(cnf_2sat_tests)))
    tests_2sat = [
        TestCase(next(test_id), expr, result, exact_check)
        for expr, result in cnf_2sat_tests.items()
    ]
    tester = TestRunner(tests_2sat, run_2sat)
    tester.run()
    results = tester.get_results()
    all_passed = tester.all_passed()
    output_msg = bar40+'\n'
    output_msg += "All Passed" if all_passed else f"Failed Tests:\n  {tester.get_failed()}"
    print(output_msg) 

if __name__ == "__main__":
    args = parse_flags()
    set_debug(args.debug)
    run_tests()
