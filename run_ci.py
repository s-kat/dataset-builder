import subprocess
import os


if __name__ == "__main__":
    cur_repo = os.environ["REPO_PATH"]
    py_env = os.environ["PY_ENV"]

    repo_name = cur_repo.split("/")[1]

    path = f"docker_volume/repos/{repo_name}"

    if py_env == 'py36':
        subprocess.run(
            f"python3 -m dataset_builder --path {path} --e {py_env}",
            shell=True,
            timeout=600,
        )
    else:
        subprocess.run(
            f"python -m dataset_builder --path {path} --e {py_env}",
            shell=True,
            timeout=600,
        ) 
