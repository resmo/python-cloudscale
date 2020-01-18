import sys
import click
from ..log import logger
from ..util import to_table, to_pretty_json
from .. import Cloudscale, CloudscaleException, CloudscaleApiException

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', envvar='CLOUDSCALE_PROFILE', help="Profile used in config file.")
@click.pass_context
def subnet(ctx, profile, api_token):
    try:
        ctx.obj = Cloudscale(api_token, profile)
    except CloudscaleException as e:
        logger.error(e)
        sys.exit(1)

@subnet.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    try:
        response = cloudscale.subnet.get_all()
        if response:
            headers = ['uuid', 'cidr', 'network', 'tags']
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)

@click.option('--uuid', required=True)
@subnet.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    try:
        response = cloudscale.subnet.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)
