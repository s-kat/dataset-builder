import csv
import subprocess

with open("repo_list.csv") as csvfile:
    reader = csv.reader(csvfile)

    for i in range(1):
        next(reader)

    for row in reader:
        cur_repo = f"{row[0]}/{row[1]}"
        subprocess.run(f"python3 run_ci.py --path {cur_repo}", shell=True, timeout=650)
