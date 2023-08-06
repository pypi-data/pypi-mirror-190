from datetime import datetime, timedelta

import click


@click.command('grow')
@click.pass_context
def grow_command(ctx):
    """Grow date time of last committed."""
    config = ctx.obj['config']

    dt = datetime.fromisoformat(config.get('commit.last-committed')) + timedelta(hours=24)

    config.set('commit.last-committed', dt.replace(hour=19, minute=0, second=0, microsecond=0).astimezone().isoformat())
    config.write()
