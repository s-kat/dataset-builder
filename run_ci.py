import argparse
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="path to repository with tox")
    args = parser.parse_args()

    cur_repo = args.path
    repo_name = cur_repo.split("/")[1]
    path = f"test_repos/{repo_name}"

    res = subprocess.run(
        f"git clone https://github.com/{cur_repo}.git {path}", shell=True
    )
    if res.returncode == 0:
        subprocess.run(
            f"python3 -m dataset_builder --path {path} --e py38",
            shell=True,
            timeout=600,
        )
