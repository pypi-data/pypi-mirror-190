import os
import json
import tempfile
from datetime import datetime, timedelta
from typing import Optional

import click


def amend_commit(src_repo, dest_repo, log, pre_cmd: Optional[str]):
    os.chdir(src_repo)
    diff_file = tempfile.mktemp()
    os.system(f'git show --binary {log["id"]} > {diff_file}')

    if pre_cmd not in ['', None]:
        pre_cmd = pre_cmd.replace("'", "\\'")
        os.system(pre_cmd.replace('{}', f"'{diff_file}'"))

    os.chdir(dest_repo)

    msg = ''.join(log['subject'])

    if os.system(f'git apply --index --whitespace=nowarn --binary {diff_file}') != 0:
        return False

    os.system('git add .')

    if os.system("git commit --message='%s' --date='%s' > /dev/null" % (msg.replace("'", "'\"'\"'"), log['date'])) != 0:
        return False

    return True


@click.command('migrate')
@click.option('-l', '--log-file', required=True, help='Path of file contains commit logs.')
@click.option('-g', '--growth', required=False, help='Time growth for each commit.')
@click.option('-e', '--execute', required=False, help='Command to execute before each commit.')
@click.argument('src_repo', type=click.Path(exists=True, file_okay=False))
@click.argument('dest_repo', type=click.Path(exists=True, file_okay=False))
@click.pass_context
def migrate_command(ctx, log_file, growth, execute, src_repo, dest_repo):
    """Migrate commit logs from a repository to another."""
    config = ctx.obj['config']

    with open(os.path.expanduser(log_file), 'r', encoding='utf-8') as fp:
        logs = reversed(json.load(fp))

    for log in logs:
        seconds = 0

        if growth is not None:
            if growth[-1] == 's':
                seconds = int(growth[:-1])
            elif growth[-1] == 'm':
                seconds = int(growth[:-1]) * 60
            elif growth[-1] == 'h':
                seconds = int(growth[:-1]) * 60 * 60
            elif growth[-1] == 'd':
                seconds = int(growth[:-1]) * 60 * 60 * 24

        delta = timedelta(seconds=seconds)

        dt = datetime.fromisoformat(log['date']) + delta

        log['date'] = dt.replace(microsecond=0).astimezone().isoformat()

        if not amend_commit(src_repo, dest_repo, log, execute):
            break
