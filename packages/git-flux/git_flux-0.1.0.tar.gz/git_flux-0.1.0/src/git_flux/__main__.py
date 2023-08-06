import click
from git_flux import __version__
from .commands.log import log


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.group()
@click.option('--version', help='Show version information.', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def cli():
    """A command-line tool to manage commits for Git repositories."""


cli.add_command(log)

if __name__ == '__main__':
    cli()
