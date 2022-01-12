import subprocess
from pathlib import Path

from dataset_builder.cli import cli_parser
from dataset_builder.config_transformer import ConfigTransformer
from dataset_builder.logger import log
from dataset_builder.result_parser import FunctionsInfo

if __name__ == "__main__":
    """
    Base pipeline:
    - transforms tox.ini config
    - runs tox with viztracer
    - extracts all functions with their arguments and outputs
    """
    args = cli_parser()

    path = args.path

    log.info(f"Transform tox.ini config")
    sections_count = ConfigTransformer(Path(f"{path}/tox.ini")).transform_tox()

    log.info(f"Run tox")
    subprocess.run(f"cd {Path(path)} && tox -e {args.e}", shell=True)

    log.info(f"Extract all functions with arguments and output")
    parser = FunctionsInfo(
        path_to_file=Path(f"{path}/result0.json"),
        path_to_repo=Path(f"{path}"),
    )
    parser.extract_functions()

    log.info(f"Dump result to {args.output}")
    parser.dump_function(Path(args.output))
