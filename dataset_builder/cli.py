import argparse


def cli_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="path to repository with tox")
    parser.add_argument("--e", help="python version for tox environment")
    args = parser.parse_args()
    return args
