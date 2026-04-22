from src.solver.cnf_ksat import run as run_ksat
from src.solver.cnf_apt import run as run_apt
from src.solver.cnf_2sat import run as run_2sat_custom
from src.solver.dp_2sat import run as run_2sat_dp


import argparse


def main():
    current_solvers = [
        run_ksat,
        run_apt,
        run_2sat_custom,
        run_2sat_dp,
    ]

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-e", "--expression", type=str, help="an expression to evaluate"
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="path to file containing one or more expressions. one expression per line",
    )
    parser.add_argument("-s", "--solver", "solver to apply")


if __name__ == "__main__":
    main()
