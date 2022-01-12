from pathlib import Path
from typing import Dict, Iterator, List, Tuple

import tree_sitter  # type: ignore
from tree_sitter import Language, Parser

# build tree sitter for python grammar
Language.build_library("build/my-languages.so", ["tree-sitter-python"])
PY_LANGUAGE = Language("build/my-languages.so", "python")

# configure parser
parser = Parser()
parser.set_language(PY_LANGUAGE)


def traverse_tree(
    tree: tree_sitter.Tree, func_lines: Dict[int, str]
) -> Iterator[Tuple[int, bytes]]:
    """Iterates tree_sitter tree and extracts text of all needed functions

    Args:
        tree: tree_sitter AST
        func_lines: Mapping <start line of function in file: function name>

    Yields:
        Iterator via tuples with start line of function and its text
    """
    cursor = tree.walk()

    reached_root = False
    while reached_root == False:
        if (
            cursor.node.type == "function_definition"
            and cursor.node.start_point[0] in func_lines
        ):
            yield (func_lines[cursor.node.start_point[0]], cursor.node.text)

        if cursor.goto_first_child():
            continue

        if cursor.goto_next_sibling():
            continue

        retracing = True
        while retracing:
            if not cursor.goto_parent():
                retracing = False
                reached_root = True

            if cursor.goto_next_sibling():
                retracing = False


def extract_functions_from_file(
    path_to_file: Path, functions: Dict[int, str]
) -> Iterator[Tuple[int, bytes]]:
    """Extracts all needed functions from file

    Args:
        path_to_file: Path to file
        functions:  Mapping <start line of function in file: function name>

    Yields:
        Iterator via tuples with start line of function and its text
    """
    with open(path_to_file, "rb") as r_file:
        tree = parser.parse(r_file.read())

    for node in traverse_tree(tree, functions):
        yield node
