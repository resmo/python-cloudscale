import click
from .. import APP_NAME
from ..version import __version__

@click.command("version")
def cmd_version():
    click.echo("%s %s" % (APP_NAME, __version__))
