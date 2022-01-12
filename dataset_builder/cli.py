import argparse


def cli_parser() -> argparse.Namespace:
    """Extracts arguments from command line

    Returns:
        Args from command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="path to repository with tox")
    parser.add_argument("--e", help="python version for tox environment")
    parser.add_argument("--output", help="name of output file")
    args = parser.parse_args()
    return args
