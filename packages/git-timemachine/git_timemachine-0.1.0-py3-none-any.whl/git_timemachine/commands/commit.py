import os
import random
from datetime import datetime, timedelta

import click


@click.command('commit')
@click.option('-m', '--message', help='Log message describing the changes.', required=True)
@click.pass_context
def commit_command(ctx, message):
    """Record a commit on a Git repository."""

    config = ctx.obj['config']

    random.seed()

    time_growth = [int(t.strip()) for t in config.get('commit.time-growth').split('-')]

    delta = timedelta(seconds=random.randint(time_growth[0], time_growth[1]))

    dt = datetime.fromisoformat(config.get('commit.last-committed')) + delta
    dt_str = dt.replace(microsecond=0).astimezone().isoformat()

    command = f'git commit -m "{message}" --date {dt_str}'

    os.system(command)

    config.set('commit.last-committed', dt_str)
    config.write()
