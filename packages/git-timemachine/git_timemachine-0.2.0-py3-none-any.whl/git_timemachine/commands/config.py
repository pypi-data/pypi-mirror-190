import sys
import os
from datetime import datetime
from configparser import NoOptionError, NoSectionError

import click
from git_timemachine.consts import CONFIG_DIR, CONFIG_FILE_NAME
from git_timemachine.helpers import Config


@click.command('config')
@click.option('--init', help='Initialize configuration file.', is_flag=True)
@click.argument('key', required=False)
@click.argument('value', required=False)
@click.pass_context
def config_command(ctx: click.Context, init: bool, key: str, value: str):
    """ Get or set configurations."""

    if init:
        os.makedirs(CONFIG_DIR, 0o755, exist_ok=True)

        config = Config(CONFIG_FILE_NAME)

        config.set('commit.last-committed', datetime.now().replace(microsecond=0).astimezone().isoformat())
        config.set('commit.time-growth', '600-3600')

        config.write()

        return

    config = ctx.obj['config']

    if key is None:
        click.echo(ctx.get_help(), err=True)

        return

    if key.find('.') == -1:
        click.echo(f'error: key does not contain a section: {key}', err=True)
        return

    if key.find('.') + 1 == len(key):
        click.echo(f'error: key does not contain variable name: {key}', err=True)
        return

    try:
        if value is None:
            sys.stdout.write(config.get(key))
            sys.stdout.write('\n')
        else:
            config.set(key, value)

            config.write()
    except (NoSectionError, NoOptionError):
        click.echo(f'error: key not found: {key}')
        return
