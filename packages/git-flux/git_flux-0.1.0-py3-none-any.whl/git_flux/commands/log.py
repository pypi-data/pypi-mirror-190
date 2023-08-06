import sys
import json
import click
from git_flux.repo import get_commit_logs


@click.command('log')
@click.argument('path', type=click.Path(exists=True, file_okay=False))
def log(path):
    """Show logs of Git repository commits."""

    sys.stdout.write(json.dumps(get_commit_logs(path), ensure_ascii=False, indent=4))
    sys.stdout.write('\n')
