import os
import json
from typing import TypedDict


class CommitLog(TypedDict):
    id: str
    author: str
    email: str
    date: str
    subject: str


def get_commit_logs(repo_dir: str) -> list[CommitLog]:
    cwd = os.getcwd()

    os.chdir(repo_dir)

    logs = [
        log.strip()
        for log in os.popen('git log --pretty=oneline --format=format:\'{"id":"%H","author":"%aN","email":"%aE","date":"%ad","subject":"%s"}\' --date=iso-strict').readlines()
    ]

    os.chdir(cwd)

    return json.loads(f'[{",".join(logs)}]')
