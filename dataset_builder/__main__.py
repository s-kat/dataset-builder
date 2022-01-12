import subprocess
from pathlib import Path

from dataset_builder.cli import cli_parser
from dataset_builder.config_transformer import ConfigTransformer
from dataset_builder.result_parser import FunctionsInfo

if __name__ == "__main__":
    args = cli_parser()

    path = args.path
    sections_count = ConfigTransformer(Path(f"{path}/tox.ini")).transform_tox()
    subprocess.run(f"cd {Path(path)} && tox -e py38", shell=True)

    parser = FunctionsInfo(
        path_to_file=Path(f"{path}/result0.json"),
        path_to_repo=Path(f"{path}"),
    )
    parser.extract_functions()
    parser.dump_function("out.json")
