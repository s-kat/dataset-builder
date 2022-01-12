import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from dataset_builder.extract_functions import extract_functions_from_file


class FunctionsInfo:
    def __init__(
        self, path_to_file: Path, path_to_repo: Path, skip_stdlib=True
    ) -> None:
        with open(path_to_file) as r_file:
            self.info = json.load(r_file)
            self.skip_stdlib = skip_stdlib
            self.path_to_repo = path_to_repo

            self.trace = self.info.get("traceEvents", [])
            self.func_names = self.info["file_info"].get("functions", {}).keys()

    def get_functions_text(self):
        for path_to_file, functions in self.total_functions.items():
            for name, text in extract_functions_from_file(
                path_to_file, {functions[i]["line"]: i for i in functions}
            ):
                functions[name]["text"] = text.decode("utf-8")

    def extract_functions(self) -> Dict[Tuple[str], List[Tuple[Optional[str]]]]:
        total_functions: Dict[Tuple[str], List[Tuple[Optional[str]]]] = {}

        for event in self.trace:
            if event["name"] in self.func_names:
                name, location = event["name"].split()
                if self.skip_stdlib and str(self.path_to_repo) not in location:
                    continue

                line = int(location[location.rfind(":") + 1 : -1]) - 1
                file_path = location[: location.rfind(":")].strip("(")

                total_functions.setdefault(file_path, {})
                total_functions[file_path].setdefault(name, {"line": line, "args": []})
                total_functions[file_path][name]["args"].append(event.get("args", {}))

        self.total_functions = total_functions
        self.get_functions_text()
        return total_functions

    def dump_function(self, out_fname: str) -> None:
        with open(out_fname, "w") as w_file:
            json.dump(self.total_functions, w_file)
