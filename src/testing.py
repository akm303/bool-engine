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

from src.solvers.cnf_2sat import run as run_2sat
from src.solvers.cnf_ksat import run as run_ksat

from src.structures.ksat import *
from src.utils.syntax import *
from src.utils.tester import *
from src.common import *



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
        title = f" ({title.title()} Check) " if title else title

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
        KEY_CHECKER: check_exact,
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
        i += 1
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
    print("Tester Passes")
    return True


# ----------------------------------------- #
# ----------------------------------------- #
# util tests

# - syntax formatting to local
syntax_to_local_test_collection = {
    KEY_LABEL: "Syntax [To Local]",
    KEY_FUNC: to_local,
    KEY_CHECKER: check_exact,
    KEY_CASES: {
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
    },
}


def syntax_from_local_tests():

    syntax_tests = {
        "latex": {
            KEY_FUNC: to_LaTeX,
            KEY_VARIANTS: [""],
            KEY_CASES: {
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
        },
        "code": {
            KEY_FUNC: to_code,
            KEY_VARIANTS: ["c", "py"],
            KEY_CASES: {
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
        },
    }

    test_collections = []
    for test_lang, test_collection in syntax_tests.items():
        updated_test_collection = None
        lang_variants = test_collection.get(KEY_VARIANTS, None)
        if lang_variants:
            for variant in lang_variants:
                updated_test_collection = {
                    KEY_LABEL: f"Syntax [to {test_lang} :: {variant}]",
                    KEY_FUNC: test_collection[KEY_FUNC],
                    KEY_CHECKER: check_exact,
                    KEY_CASES: {
                        (test_input, variant): test_expected
                        for test_input, test_expected in test_collection[
                            KEY_CASES
                        ].items()
                    },
                }
        else:
            updated_test_collection = (
                {
                    KEY_LABEL: f"Syntax [to {test_lang}]",
                    KEY_FUNC: test_collection[KEY_FUNC],
                    KEY_CHECKER: check_exact,
                    KEY_CASES: test_collection[KEY_CASES],
                },
            )

            test_collections.append(updated_test_collection)
            print("syntax test collection:")
            print_test_collection(test_collections[-1])
    return test_collections


syntax_tests = [syntax_to_local_test_collection] + syntax_from_local_tests()

# total_results = []
# for test_lang, test_cases in syntax_tests.items():
#     if test_lang == "code":
#         for i, lang in enumerate(["py", "c"]):
#             print(f"testing for conversion to {test_lang}::{lang}")
#             for test_case, test_expected in test_cases.items():
#                 test_expected = test_expected.replace("&", "&" * (i + 1))
#                 test_expected = test_expected.replace("|", "|" * (i + 1))
#                 test_actual = test_funcs[test_lang](test_case, lang)
#                 case_passed = check_exact(test_case, test_expected, test_actual)
#                 total_results.append(case_passed)
#                 # total_results.append((test_case,test_expected,test_actual,case_passed))
#     else:
#         print(f"testing for conversion to {test_lang}")
#         for test_case, test_expected in test_cases.items():
#             test_actual = test_funcs[test_lang](test_case)
#             case_passed = check_exact(test_case, test_expected, test_actual)
#             total_results.append(case_passed)
# return total_results


# def test_syntax():
# def to_local_test():
#     test_collection = {
#         KEY_LABEL: "Syntax [To Local]",
#         KEY_FUNC: to_local,
#         KEY_CHECKER: check_exact,
#         KEY_CASES: {
#             # and-based cases
#             r"a&a": "a.a",
#             r"a&&b": "a.b",
#             r"a.c": "a.c",
#             r"a\land d": "a.d",
#             r"a\lande": "a.e",
#             # or-based cases
#             r"a|a": "a+a",
#             r"a||b": "a+b",
#             r"a+c": "a+c",
#             r"a\lor d": "a+d",
#             r"a\lore": "a+e",
#         },
#     }

# total_results = []
# for test_case, test_expected in local_syntax_tests.items():
#     test_actual = to_local(test_case)
#     case_passed = check_exact(test_case, test_expected, test_actual)
#     total_results.append(case_passed)
# return total_results

# def from_local_test():
#     syntax_tests = {
#         "latex": {
#             # and-based cases
#             r"a&a": r"a\land a",
#             r"a&&b": r"a\land b",
#             r"a.c": r"a\land c",
#             r"a\land d": r"a\land d",
#             r"a\lande": r"a\land e",
#             # or-based cases
#             r"a|a": r"a\lor a",
#             r"a||b": r"a\lor b",
#             r"a+c": r"a\lor c",
#             r"a\lor d": r"a\lor d",
#             r"a\lore": r"a\lor e",
#         },
#         "code": {
#             # and-based cases
#             r"a&a": "a&a",
#             r"a&&b": "a&b",
#             r"a.c": "a&c",
#             r"a\land d": "a&d",
#             r"a\lande": "a&e",
#             # or-based cases
#             r"a|a": "a|a",
#             r"a||b": "a|b",
#             r"a+c": "a|c",
#             r"a\lor d": "a|d",
#             r"a\lore": "a|e",
#         },
#     }

#     test_funcs = {
#         "latex": to_LaTeX,
#         "code": to_code,
#     }

#     total_results = []
#     for test_lang, test_cases in syntax_tests.items():
#         if test_lang == "code":
#             for i, lang in enumerate(["py", "c"]):
#                 print(f"testing for conversion to {test_lang}::{lang}")
#                 for test_case, test_expected in test_cases.items():
#                     test_expected = test_expected.replace("&", "&" * (i + 1))
#                     test_expected = test_expected.replace("|", "|" * (i + 1))
#                     test_actual = test_funcs[test_lang](test_case, lang)
#                     case_passed = check_exact(test_case, test_expected, test_actual)
#                     total_results.append(case_passed)
#                     # total_results.append((test_case,test_expected,test_actual,case_passed))
#         else:
#             print(f"testing for conversion to {test_lang}")
#             for test_case, test_expected in test_cases.items():
#                 test_actual = test_funcs[test_lang](test_case)
#                 case_passed = check_exact(test_case, test_expected, test_actual)
#                 total_results.append(case_passed)
#     return total_results

# print("Running Tests:")
# total_results = []
# total_results += to_local_test()
# total_results += from_local_test()

# final_result = all(r == True for r in total_results)
# print(f"\nAll test cases passed? {final_result}")
# return final_result


# ----------------------------------------- #
# ----------------------------------------- #
# src util tests
to_2sat_collection = {
    KEY_LABEL: "Helper Function: to_2sat()",
    KEY_FUNC: test_to_2sat,
    KEY_CHECKER: check_exact,
    KEY_CASES: {
        # custom examples
        "(x)": [["x", "x"]],
        "(x,x)": [["x", "x"]],
        "(x,x,x)": None,
        "(x,x)(x)": [["x", "x"],["x", "x"]],
        "(x,x)(x,x)": [["x", "x"],["x", "x"]],
        "(x,x)(x,x,x)": None,
        "(x,x,x)(x,x)": None
    },
}

# src tests
cnf_2sat_collection = {
    KEY_LABEL: "2SAT Solver",
    KEY_FUNC: run_2sat,
    KEY_CHECKER: check_exact,
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
    KEY_CHECKER: check_exact,
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
sat_tests = [to_2sat_collection, cnf_2sat_collection, cnf_ksat_collection]


def run_test(test_hook, all_passed_hook=None, test_title="Test: ???"):
    print(f"## running: {test_title}")
    print(bar40)
    print("```tex")

    results = test_hook()

    output_msg = "\n >>> "
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
    print("```")
    print()

    print(bar40)
    print(f"## completed: {test_title}")
    print()
    print()
    return results


if __name__ == "__main__":
    print("running `testing.py")
    print()
    args = parse_flags()
    set_debug(args.debug)

    # array of test functions (callable) or collections (dict) to be ran
    # if function, runs test directly
    # if collection, sets up and runs test

    all_tests = [tester_test] + syntax_tests + sat_tests

    results = {}
    for i, test in enumerate(all_tests):

        test_hook = None
        all_passed_hook = None

        if isinstance(test, dict):
            tester = setup_test(test)

            test_title = tester.label
            test_hook = tester.run_all
            all_passed_hook = tester.all_passed

        else:  # is function
            test_title = f"`{test.__name__}()`"
            test_hook = test

        result = run_test(test_hook, all_passed_hook, test_title)
        results[test_title] = result
        # print()

    if all(r == True for r in results.values()):
        print("All tests passed")
    else:
        print("some tests failed")
        failed_tests = [
            f"{test_title}: {test_result}"
            for test_title, test_result in results.items()
            if test_result != True
        ]
        print(f"{failed_tests}")

else:
    print("importing `testing.py")
