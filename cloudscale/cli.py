import click
from .util import OrderedGroup
from .commands.version import cmd_version
from .commands.server import server
from .commands.server_group import server_group
from .commands.flavor import flavor
from .commands.floating_ip import floating_ip
from .commands.image import image
from .commands.region import region
from .commands.network import network


@click.group(cls=OrderedGroup, context_settings={
    "help_option_names": ["-h", "--help"],
})
def cli():
    pass

cli.add_command(cmd_version)
cli.add_command(server)
cli.add_command(server_group)
cli.add_command(floating_ip)
cli.add_command(flavor)
cli.add_command(image)
cli.add_command(region)
cli.add_command(network)
