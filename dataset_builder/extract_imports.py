import ast
from pathlib import Path
from typing import List

from stdlib_list import stdlib_list


def extract_imports_from_file(path_to_file: Path) -> List[str]:
    """Extracts all imports from file

    Arguments:
        path_to_file: path to file

    Returns:
        List with imports
    """
    with open(path_to_file, "r") as r_file:
        code = r_file.read()

    imports = []
    # extract only stdlib imports
    libraries = set(stdlib_list("3.8"))

    for node in ast.iter_child_nodes(ast.parse(code)):
        if (
            isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.module.split(".")[0] in libraries
        ):
            imports.append(ast.get_source_segment(code, node))
        elif isinstance(node, ast.Import) and node.names[0].name in libraries:
            imports.append(ast.get_source_segment(code, node))

    return imports
