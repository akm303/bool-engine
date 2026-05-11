import os
import inspect
import shutil
import pathlib
from pathlib import Path
from typing import Callable


# --------------------------------------------------- #
# Printout Logs/Stdout
TO_LOG = True
OVERWRITE_FILES = True
COMPACT = True  # compact strings
EXPANDED = not COMPACT  # expanded output (verbose)

OUTPUT_DIRECTORY = ".outputs"


def reset_directory(out_dir:str):
    protected = ["src",".venv",".archive"]

    if any(term in out_dir.lower() for term in protected):
        print(f"'{out_dir}' is protected")
        return
    
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)  # Deletes the folder and everything in it
    os.makedirs(out_dir)       # Recreates an empty folder
        
        
def clear_directory(directory):
    """removes directory from filesystem"""
    directory = Path(directory)
    try:
        shutil.rmtree(directory)
        print(f"Removed directory '{directory}' and contents.")
    except OSError as e:
        print(f"\nError: {directory} : {e.strerror}")


def print_to_file(printer: Callable, output_dir=OUTPUT_DIRECTORY):
    """
    Writes output to stdout and to specified file in output directory
    note: running files from root directory => output_files must be wrt root directory

    Add line to top of script for any print function (print || dprint) for which
    statements are to be collectively written to file
    eg. `dprint = print_to_file(dprint, "debug/debug_outputs.tex")`
    """

    # ---- #
    clear_directory(output_dir) # resetting output file
    output_file = f"{output_dir}/output.md"

    if not TO_LOG:
        return printer

    def wrapped_printer(*args, **kwargs):
        outpath = os.path.dirname(output_file)
        os.makedirs(outpath, exist_ok=True)

        printer(*args, **kwargs)  # print to terminal

        with open(output_file, "a") as f:
            fkwargs = dict(kwargs)  # print to file
            fkwargs["file"] = f
            printer(*args, **fkwargs)

    # wrapped_printer._is_wrapped = True
    return wrapped_printer


base_print = print
print = print_to_file(print)