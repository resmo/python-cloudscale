import sys
import click
from ..log import logger
from ..util import to_table
from .. import Cloudscale, CloudscaleApiException, CloudscaleException

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', help="Profile used in config file.")
@click.pass_context
def image(ctx, profile, api_token):
    try:
        ctx.obj = Cloudscale(api_token, profile)
    except CloudscaleException as e:
        logger.error(e)
        sys.exit(1)

@image.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    try:
        response = cloudscale.image.get_all()
        if response:
            headers = ['name', 'operating_system', 'default_username', 'slug']
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)
