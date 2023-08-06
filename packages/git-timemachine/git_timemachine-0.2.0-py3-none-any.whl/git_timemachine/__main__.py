import os
import click
from . import __version__

from .consts import CONFIG_FILE_NAME
from .commands import config_command, commit_command, grow_command, log_command, migrate_command
from .helpers import Config


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return

    click.echo(__version__)
    ctx.exit()


@click.group()
@click.option('--version', help='Show version information.', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.pass_context
def cli(ctx):
    """A command-line tool to manage commits for Git repositories."""

    ctx.ensure_object(dict)

    ctx.obj['config'] = Config(CONFIG_FILE_NAME)

    if os.path.exists(CONFIG_FILE_NAME):
        ctx.obj['config'].read()


cli.add_command(config_command)
cli.add_command(commit_command)
cli.add_command(grow_command)
cli.add_command(log_command)
cli.add_command(migrate_command)

if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    cli(obj={})
