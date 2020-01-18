import sys
import click
from ..log import logger
from ..util import to_table
from .. import Cloudscale, CloudscaleApiException, CloudscaleException

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', help="Profile used in config file.")
@click.pass_context
def region(ctx, profile, api_token):
    try:
        ctx.obj = Cloudscale(api_token, profile)
    except CloudscaleException as e:
        logger.error(e)
        sys.exit(1)

@region.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    try:
        response = cloudscale.region.get_all()
        if response:
            headers = ['zones', 'slug']
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)
