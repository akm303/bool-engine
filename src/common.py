"""
Docstring for src.common

type definitions, constants, and functions common across project
"""

import re
import argparse
from typing import Callable, Iterable, Collection, Tuple

# --------------------------------------------------- #
# debug helpers
DEBUG_PRINT = False
# DEBUG_PRINT = True


def set_debug(to_debug: bool):
    """
    sets global DEBUG_PRINT constant to true
    (currently applied only with parsed args)
    """
    global DEBUG_PRINT
    DEBUG_PRINT = to_debug


def dprint(*args, **kwargs):
    """debug print: prints statements only if global DEBUG_PRINT constant set to true"""
    # args = ' >> debug:',*args
    if DEBUG_PRINT:
        print(*args, **kwargs)


def sfmt(*varlist: list, fmt=str) -> list[str]:
    """format string for every element in list"""
    return [fmt(var) for var in varlist]


def dfmt(*varlist: list, fmt=str) -> list:
    """format string for debug prints if debug enabled, otherwise return as is"""
    return varlist if not DEBUG_PRINT else sfmt(varlist, fmt=fmt)


def parse_debug_flag():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


# --------------------------------------------------- #
# Expression type aliases
expression_type = str
variable_type = str
literal_type = variable_type
clause_type = list[literal_type]

e_type = expression_type
v_type = variable_type
l_type = literal_type
c_type = clause_type

# -------------------------------- #
# Graph type aliases
node_type = str
edge_type = Tuple[str, str]
graph_type = dict[node_type, set[node_type]]

# -------------------------------- #
# Result type aliases
a_type = dict  # a = assignment


# --------------------------------------------------- #
# String helpers (matching / formatting)

# -------------------------------- #
# regex string patterns
SUBEXPR_PATTERN = r"\([^()]+\)"
LITERAL_PATTERN = r"(\w+'?)"  # r"(x_\d+'?)"
# SATSOLVER_VARIABLE_PATTERN = r"(\w+)'?"  # r"(x_\d+'?)" #todo: test
TRANSFORM_VARIABLE_PATTERN = r"X\d+"
ASSIGNMENT_PATTERN = r":?="


# -------------------------------- #
# common string constructors
def bar(n):
    return "-" * n


bar40 = bar(40)


# --------------------------------------------------- #
# formatting helper functions
def bool_num(value: bool) -> int:
    """returns int representing bool value"""
    assert isinstance(value, bool)
    return 1 if value is True else 0


# --------------------------------------------------- #
# string formatting


# -------------------------------- #
# canonical collection formatting
def collection_str(
    objs: Collection,
    obj_fmt: Callable,
    delim: str = ", ",
    output_type=None,
) -> str:
    """formats a collection of objects"""

    # select correct braces format
    braces_map = {
        tuple: r"()",
        list: r"[]",
        set: r"{}",
    }
    if output_type and output_type in braces_map:
        braces = braces_map[output_type]
    else:
        braces = braces_map[type(objs)]

    return braces[0] + delim.join([obj_fmt(obj) for obj in objs]) + braces[1]


# -------------------------------- #
# graph - objects
def node_str(node: node_type) -> str:
    """generates a string representing a node containing a literal"""
    return node if is_complement(node) else node + " "


def edge_str(edge: edge_type) -> str:
    """generates a string representing an edge containing a pair of nodes"""
    return f"( {node_str(edge[0])}, {node_str(edge[1])})"


def adjgraph_str(
    adj_graph: graph_type, indent: str = " ", one_line: bool = False
) -> str:
    spacer: str = "\n" if not one_line else " "
    terms = []
    for node, adj_nodes in adj_graph.items():
        terms.append(f"{indent}{node_str(node)}: {nodeset_str(adj_nodes)}")
    outstring = f",{spacer}".join(terms)
    return f"{{{spacer}{outstring}{spacer}}}"


# -------------------------------- #
# graph - collections
def nodes_str(nodes: Collection[node_type], delim=", ", output_type=list) -> str:
    return collection_str(nodes, node_str, delim=delim, output_type=output_type)


def edges_str(nodes: list[edge_type], delim=", ", output_type=list) -> str:
    return collection_str(nodes, edge_str, delim=delim, output_type=output_type)


def nodelist_str(nodes: list[node_type]) -> str:
    return nodes_str(nodes, output_type=list)


def edgelist_str(edges: list[edge_type]) -> str:
    return edges_str(edges, output_type=list)


def nodeset_str(nodes: set[node_type]) -> str:
    return nodes_str(nodes, output_type=set)


def edgeset_str(edges: list[edge_type]) -> str:
    return edges_str(edges, output_type=set)


# -------------------------------- #
# expression - objects
def variable_str(variable: v_type) -> str:
    """generates a string representing a variable"""
    return variable


# ! ^redundant; variables are already strings without need for formatting,
# ! or use literal formatting


def literal_str(literal: l_type) -> str:
    """generates a string representing a literal"""
    return literal if is_complement(literal) else literal + " "


def clause_str(clause: c_type) -> str:
    """generates a string representing a clause"""
    return f"({f' + '.join(clause)})"


# -------------------------------- #
# expression - collections
def variables_str(variables: Collection[v_type], delim=", ", output_type=list) -> str:
    """generates a string representing a list of variables"""
    return collection_str(variables, obj_fmt=str, delim=delim, output_type=output_type)


def literals_str(literals: Collection[l_type], delim=", ", output_type=set) -> str:
    """generates a string representing a collection of variables/literals"""
    return collection_str(
        sorted(list(literals)),
        obj_fmt=literal_str,
        delim=delim,
        output_type=output_type,
    )


def clauses_str(clauses: Collection[c_type], delim=", ", output_type=list) -> str:
    """generates a string representing a collection of clauses"""
    return collection_str(
        clauses, obj_fmt=clause_str, delim=delim, output_type=output_type
    )


def assignment_str(assignment: a_type) -> str:
    """generates a string representing an assignment of boolean values to variables"""
    return f"{{ {', '.join([f'{k} : {v} ' for k, v in assignment.items()] if assignment else [])}}}"


# --------------------------------------------------- #
def to_syntax(string: str, target_syntax: str):

    target_syntax = target_syntax.lower()
    string = string.replace(" ", "")

    CANON_OR = " OR "
    CANON_AND = " AND "

    # convert to a intermediate canonical form
    string = re.sub(r"(\\lor|\|\||\||\+)", CANON_OR , string)
    string = re.sub(r"(\\land|&&|&|\.)", CANON_AND, string)

    or_op = "+"
    and_op = "."
    if target_syntax in ["latex"]:
        or_op = r"\lor "
        and_op = r"\land "
    elif target_syntax in ["c", "cpp", "c++"]:
        or_op = "||"
        and_op = "&&"
    elif target_syntax in ["py", "python"]:
        or_op = "|"
        and_op = "&"

    string = string.replace(CANON_OR, or_op)
    string = string.replace(CANON_AND, and_op)
    return string



def to_local(string: str) -> str:
    return to_syntax(string,"local")

def to_LaTeX(string: str) -> str:
    return to_syntax(string,"latex")

def to_code(string:str,lang:str) -> str:
    return to_syntax(string,lang)



# --------------------------------------------------- #
# common boolean-logic helpers


def is_complement(literal: l_type) -> bool:
    return "'" in literal


def neg(literal: l_type) -> l_type:
    return (
        literal + "'" if literal == base_variable(literal) else literal.replace("'", "")
    )


def base_variable(literal: l_type) -> v_type:
    return literal.replace("'", "")


# --------------------------------------------------- #
# --------------------------------------------------- #
# tests


def check_testcase(original, expected, actual):
    case_passed = expected == actual
    original = f'"{original}"'
    print(
        f'  case {original:10}: expected("{expected}") == actual("{actual}")? '
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
            case_passed = check_testcase(test_case, test_expected, test_actual)
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
                        case_passed = check_testcase(
                            test_case, test_expected, test_actual
                        )
                        total_results.append(case_passed)
                        # total_results.append((test_case,test_expected,test_actual,case_passed))
            else:
                print(f"testing for conversion to {test_lang}")
                for test_case, test_expected in test_cases.items():
                    test_actual = test_funcs[test_lang](test_case)
                    case_passed = check_testcase(test_case, test_expected, test_actual)
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
    args = parse_debug_flag()
    set_debug(args.debug)
    # set_test(True)
    test_syntax()
