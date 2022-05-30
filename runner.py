import csv
import subprocess
import configparser
from time import sleep

def get_python_env(path_to_config):
    try:
        config = configparser.ConfigParser()
        config.read(path_to_config)
        envs = config['tox']['envlist']
        if '38' in envs:
            return 'py38'
        elif '36' in envs:
            return 'py36'
        elif '37' in envs:
            return 'py37'
        elif '39' in envs:
            return 'py39'
        else:
            return 'py38'
    except:
        return 'py38'

if __name__ == "__main__":
    with open("good_repo_list.csv") as r_file:
        repos = csv.reader(r_file)

        next(repos)
        for j, i in enumerate(repos):
            if j >= 10:
                exit()
            cur_repo = f"{i[0]}/{i[1]}"
            repo_name = cur_repo.split("/")[1]
            path = f"docker_volume/repos/{repo_name}"
            docker_ps = subprocess.run("docker ps", shell=True, capture_output=True, text=True).stdout.strip().count('runner_')
            while docker_ps > 2:
                print(f"{docker_ps} CONTAINERS: WAIT")
                sleep(10)
                docker_ps = subprocess.run("docker ps", shell=True, capture_output=True, text=True).stdout.strip().count('runner_')

            res = subprocess.run(
                f"git clone https://github.com/{cur_repo}.git {path}", shell=True
            )
            if res.returncode == 0:
                py_env = get_python_env(f'docker_volume/repos/{repo_name}/tox.ini')
                cur_path = subprocess.run("pwd", shell=True, capture_output=True, text=True).stdout.strip()
                print(f"docker run -d -e REPO_PATH='{cur_repo}' -e PY_ENV='{py_env}' -v {cur_path}/docker_volume:/usr/app/src/docker_volume --rm runner_{py_env}", flush=True)
                subprocess.run(
                    f"docker run -d -e REPO_PATH='{cur_repo}' -e PY_ENV='{py_env}' -v {cur_path}/docker_volume:/usr/app/src/docker_volume --rm runner_{py_env}",
                    shell=True
                )
