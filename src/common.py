"""
Docstring for src.common

type definitions, constants, and functions common across project
"""

import re
import argparse

# --------------------------------------------------- #
# type aliases
e_type = str  # e = expression
c_type = list[int]  # c = clause
v_type = str  # v = variable
l_type = v_type  # l = literal


# regex patterns
SUBEXPR_PATTERN = r"\([^()]+\)"
LITERAL_PATTERN = r"(\w+'?)"  # r"(x_\d+'?)"
# SATSOLVER_VARIABLE_PATTERN = r"(\w+)'?"  # r"(x_\d+'?)" #todo: test
TRANSFORM_VARIABLE_PATTERN = r"X\d+"
ASSIGNMENT_PATTERN = r":?="

# --------------------------------------------------- #
# debug print
DEBUG_PRINT = False
# DEBUG_PRINT = True

def set_debug(to_debug: bool):
    global DEBUG_PRINT
    DEBUG_PRINT = to_debug

def dprint(*args, **kwargs):
    if DEBUG_PRINT:
        print(*args, **kwargs)

def parse_debug_flag():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--debug',action='store_true')
    return parser.parse_args()


# --------------------------------------------------- #
# string formatting
def bar(n):
    return "-" * n


bar40 = bar(40)


def c_str(clause):
    """generates a string representing a clause"""
    return f"({f' + '.join(clause)})"


def clist_str(clauses: list[list[v_type]]):
    """generates a string representing a list of clauses"""
    # djunc_delim = ' * '
    djunc_delim = ", "
    # djunc_delim = ' '
    rstr = [c_str(clause) for clause in clauses]
    return f"[{djunc_delim.join(rstr)}]"


def vlist_str(variable_list):
    """generates a string representing a list of variables"""
    return f"[ {f', '.join(variable_list)} ]"


def a_str(assignment: dict):
    """generates a string representing an assignment of boolean values to variables"""
    if not assignment:
        return None
    rstr = [f"{k} : {v}" for k, v in assignment.items()]
    rstr = f"{{ {', '.join(rstr)} }}"
    return rstr


# syntax conversions
def to_local_syntax(string: str):
    operator_map = {
        r"\lor": "+",
        r"||": "+",
        r"|": "+",
        r"\land": ".",
        r"&&": ".",
        r"&": ".",
    }
    for latex_op, local_op in operator_map.items():
        string = string.replace(latex_op, local_op)
    string = string.replace(" ", "")
    return string


def to_LaTeX(string: e_type):
    string = to_local_syntax(string)
    operator_map = {
        r"\lor ?": r"\land ",
        "||": r"\lor ",
        "|": r"\lor ",
        "+": r"\lor ",
        r"\land ?": r"\land ",
        "&&": r"\land ",
        "&": r"\land ",
        ".": r"\land ",
    }
    for local_op, code_op in operator_map.items():
        string = string.replace(local_op, code_op)
    return string


    # for varstr in list(variables):
    #     string.replace(r"\w+'?", rf"\\neg{varstr}")
    # string.replace(" ", "")
    # return string


def to_code(string: str, language: str):
    dprint(f"  string: {string}")
    string = to_local_syntax(string)
    dprint(f"  to local: {string}")

    is_python = language.lower() in ["py", "python"]
    is_c = language.lower() in ["c", "c++", "cpp"]

    or_op = "|"
    and_op = "&"
    if is_c:
        or_op = '||'
        and_op = '&&'

    operator_map = {
        r"\lor": or_op,
        "||": or_op,
        "|": or_op,
        "+": or_op,
        r"\land": and_op,
        "&&": and_op,
        "&": and_op,
        ".": and_op,
    }
    dprint(f"  to {language} string:")
    for local_op, code_op in operator_map.items():
        string = string.replace(local_op, code_op)
        # string2 = string.replace(local_op, code_op)
        # dprint(f"  \"{string}\" (replacing \'{local_op}\' with \'{code_op}\') => \"{string2}\"")
        # string = string2
    return string


# --------------------------------------------------- #
# common boolean-logic helpers


def is_complement(literal: l_type) -> bool:
    return "'" in literal


def base_variable(literal: l_type) -> v_type:
    return literal.replace("'", "")


# --------------------------------------------------- #
# --------------------------------------------------- #
# tests


def check(original,expected, actual):
    case_passed = expected == actual
    original = f'"{original}"'
    print(
        f"  case {original:10}: expected(\"{expected}\") == actual(\"{actual}\")? "
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
            test_actual = to_local_syntax(test_case)
            case_passed = check(test_case,test_expected,test_actual)
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
                for i,lang in enumerate(["py", "c"]):
                    print(f"testing for conversion to {test_lang}::{lang}")
                    for test_case, test_expected in test_cases.items():
                        test_expected = test_expected.replace('&','&'*(i+1))
                        test_expected = test_expected.replace('|','|'*(i+1))
                        test_actual = test_funcs[test_lang](test_case, lang)
                        case_passed = check(test_case,test_expected,test_actual)
                        total_results.append(case_passed) 
                        # total_results.append((test_case,test_expected,test_actual,case_passed))
            else:
                print(f"testing for conversion to {test_lang}")
                for test_case, test_expected in test_cases.items():
                    test_actual = test_funcs[test_lang](test_case)
                    case_passed = check(test_case,test_expected,test_actual)
                    total_results.append(case_passed) 
        return total_results
    
    print("Running Tests:")
    total_results = []
    total_results += to_local_test()
    total_results += from_local_test()

    final_result = all(r == True for r in total_results)
    print(f"\nAll test cases passed? {final_result}")
    return total_results


if __name__ == "__main__":
    # args = parse_debug_flag()
    # set_debug(args.debug)
    test_syntax()
