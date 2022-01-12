from pathlib import Path
from typing import Iterator, List, Tuple

from tree_sitter import Language, Parser  # type: ignore

Language.build_library("build/my-languages.so", ["tree-sitter-python"])
PY_LANGUAGE = Language("build/my-languages.so", "python")

parser = Parser()
parser.set_language(PY_LANGUAGE)


def traverse_tree(tree, func_lines) -> Iterator[Tuple[int, bytes]]:
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
    path_to_file: Path, functions: List[int]
) -> Iterator[Tuple[int, bytes]]:
    with open(path_to_file, "rb") as r_file:
        tree = parser.parse(r_file.read())
    for node in traverse_tree(tree, functions):
        yield node
