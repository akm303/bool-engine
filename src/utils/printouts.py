import os
import inspect
import shutil
import pathlib
from typing import Callable


# --------------------------------------------------- #
# Printout Logs/Stdout
TO_LOG = True
OVERWRITE_FILES = True
# TEST_DIRECTORY = "tests"
# OUTPUT_DIRECTORY = ".outputs"
# BASE_TEST_FILENAME = "-test.tex"
# BASE_DEBUG_FILENAME = "-debug.tex"
COMPACT = True  # compact strings
EXPANDED = not COMPACT  # expanded output (verbose)

OUTPUT_DIRECTORY = ".outputs"



# def init_output_dir(output_dir:str = OUTPUT_DIRECTORY):
#     base_print(f'0. initializing output directory: "{output_dir}/"')
#     if OVERWRITE_FILES and os.path.exists(output_dir):
#         base_print(f'   clearing previous directory: "{output_dir}/"')
#         shutil.rmtree(output_dir)
#     base_print(f'   making directory: "{output_dir}/"')
#     os.makedirs(output_dir, exist_ok=True)


def get_calling_module() -> str:
    frame = inspect.stack()[2]  # caller of wrapped printer
    module = inspect.getmodule(frame[0])
    if module:
        # module_name = module.__name__.split(".")[-1]
        # base_print(f"module_name: {module_name}")

        # return module.__name__
        
        return module.__name__.split(".")[-1]
    return "unknown"


# def print_to_file(printer: Callable, output_dir: str | None = OUTPUT_DIRECTORY):
def print_to_file(printer: Callable, output_dir = OUTPUT_DIRECTORY):
    """
    Writes output to stdout and to specified file in output directory
    note: running files from root directory => output_files must be wrt root directory

    Add line to top of script for any print function (print || dprint) for which
    statements are to be collectively written to file
    eg. `dprint = print_to_file(dprint, "debug/debug_outputs.tex")`
    """
    # base_print(f'print_to_file: {printer}, "{output_dir}"')
    if getattr(printer, "_is_wrapped", False):
        return printer

    # log_file = f"{OUTPUT_DIRECTORY}/log_file"
    # debug_file = f"{OUTPUT_DIRECTORY}/debug_file"
    # test_file = f"{OUTPUT_DIRECTORY}/test_file"

    # def resolve_output_file(output_file):
    #     valid_suffix = [".tex", ".txt", ".md"]
    #     if output_file:
    #         if pathlib.Path(output_file).suffix not in valid_suffix:
    #             output_file = pathlib.Path.with_suffix(".tex")
    #         return f"{OUTPUT_DIRECTORY}/{output_file}"

    #     caller = get_calling_module()
    #     return

    # output_file = resolve_output_file(output_file)

    # if OVERWRITE_FILES:
    #     open(output_file, "w").close()

    # ---- #
    caller = get_calling_module()
    output_file = f"{output_dir}/{caller}.md"
    # base_print(f'1. output_dir + caller: "{output_dir}" + "{caller}" -> output_file: "{output_file}"')

    if not TO_LOG:
        return printer

    def wrapped_printer(*args, **kwargs):
        # caller = get_calling_module()
        # output_file = f"{output_dir}/{caller}.md"
        # base_print(f'1. output_dir + caller: "{output_dir}" + "{caller}" -> output_file: "{output_file}"')

        # caller = get_calling_module()
        # output_file = f"{OUTPUT_DIRECTORY}/{caller}.md"
        
        outpath = os.path.dirname(output_file)
        # base_print(f'2. outpath: "{outpath}" -> output_file "{output_file}"')
        os.makedirs(outpath, exist_ok=True)
        # base_print(f'   os.makedirs("{outpath}",exist_ok=True)')

        printer(*args, **kwargs)  # print to terminal

        with open(output_file, "a") as f:
            fkwargs = dict(kwargs)  # print to file
            fkwargs["file"] = f
            printer(*args, **fkwargs)

    wrapped_printer._is_wrapped = True
    return wrapped_printer



# test outputs to tests directory
# print = print_to_file(print, "stdout/common.tex")

# def print_to_file(printer: Callable, output_file: str|None = None):
#     """
#     Writes output to stdout and to specified file in output directory
#     note: running files from root directory => output_files must be wrt root directory

#     Add line to top of script for any print function (print || dprint) for which
#     statements are to be collectively written to file
#     eg. `dprint = print_to_file(dprint, "debug/debug_outputs.tex")`
#     """

#     # log_file = f"{OUTPUT_DIRECTORY}/log_file"
#     # debug_file = f"{OUTPUT_DIRECTORY}/debug_file"
#     # test_file = f"{OUTPUT_DIRECTORY}/test_file"

#     def resolve_output_file(output_file):
#         valid_suffix = [".tex", ".txt", ".md"]
#         if output_file:
#             if pathlib.Path(output_file).suffix not in valid_suffix:
#                 output_file = pathlib.Path.with_suffix(".tex")
#             return f"{OUTPUT_DIRECTORY}/{output_file}"

#         caller = get_calling_module()
#         return f"{OUTPUT_DIRECTORY}/{caller}.tex"

#     output_file = resolve_output_file(output_file)

#     os.makedirs(os.path.dirname(output_file), exist_ok=True)

#     if OVERWRITE_FILES:
#         open(output_file, "w").close()

#     if TO_LOG:
#         def wrapped_printer(*args, **kwargs):
#             printer(*args, **kwargs)  # print to terminal

#             with open(output_file, "a") as f:
#                 fkwargs = dict(kwargs)  # print to file
#                 fkwargs["file"] = f
#                 printer(*args, **fkwargs)

#         return wrapped_printer
#     return printer


# # test outputs to tests directory
# print = print_to_file(print, "stdout/common.tex")

