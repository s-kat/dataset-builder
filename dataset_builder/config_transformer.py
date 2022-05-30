import configparser
from pathlib import Path
from typing import List, Optional

from dataset_builder.constants import ToxConfig


class ConfigTransformer:
    """Transforms tox.ini config for tracing functions"""

    def __init__(self, path_to_config: Path) -> None:
        self.path_to_config = path_to_config
        self.config = configparser.ConfigParser()
        self.config.read(path_to_config)
        self.results: List[Path] = []
        self.sections_with_pytest = 0

    def set_tracer(self, section: str) -> Optional[str]:
        """Tries to find pytest in config section, in case of success adds viztracer command and dependency

        Args:
            section: config section name

        Returns:
            Name of file with results of tracing, or None
        """
        section_commands = self.config[section].get("commands", "")
        res_file = None

        # try to find pytest
        inj_ind = max(section_commands.find("py.test"), section_commands.find("pytest"))

        if inj_ind != -1:
            res_file = f"result{self.sections_with_pytest}.json"

            cur_commands = (
                section_commands[: inj_ind if inj_ind - 1 >= 0 else 0]
                + ToxConfig.INJECTION_TRACE
                + f" -o {res_file} -- "
                + section_commands[inj_ind:]
            )

            self.config[section]["commands"] = cur_commands
            self.sections_with_pytest += 1

            # add viztracer to deps
            self.config[section].setdefault("deps", "")
            self.config[section]["deps"] += "\ngit+https://github.com/s-kat/viztracer.git "

        return res_file

    def transform_tox(self) -> List[Path]:
        """Transforms tox.ini config for tracing functions

        Returns:
            List with files with results of tracing function

        """
        for section in self.config.sections():
            out_fname = self.set_tracer(section)
            if out_fname is not None:
                self.results.append(self.path_to_config.parent / out_fname)

        self.save_config()
        return self.results

    def save_config(self) -> None:
        """Saves transformed config"""
        with open(self.path_to_config, "w") as config_file:
            self.config.write(config_file)
