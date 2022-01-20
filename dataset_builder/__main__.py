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
    tracing_results_path = ConfigTransformer(Path(f"{path}/tox.ini")).transform_tox()

    log.info(f"Run tox")

    if args.e is not None:
        tox_command = f"tox -e {args.e}"
    else:
        tox_command = "tox"

    subprocess.run(f"cd {Path(path)} && {tox_command}", shell=True)

    log.info(f"Extract all functions with arguments and output")
    for i, res_path in enumerate(tracing_results_path):
        if Path(res_path).is_file():
            parser = FunctionsInfo(
                path_to_file=res_path,
                path_to_repo=Path(path),
            )
            parser.extract_functions()
            log.info("filter functions")
            parser.filter_functions()
            log.info(f"Dump result to {path}_res{i}.json")
            parser.dump_function(Path(f"result/{Path(path).name}_res{i}.json"))
