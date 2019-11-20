import sys
import click
from ..util import to_table
from .. import Cloudscale, CloudscaleApiException, CloudscaleException

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def network(ctx, api_token, verbose):
    try:
        ctx.obj = Cloudscale(api_token)
        ctx.obj.verbose = verbose
    except CloudscaleException as e:
        click.echo(e, err=True)
        sys.exit(1)

@network.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    try:
        response = cloudscale.network.get_all()
        if response:
            headers = ['name', 'created_at', 'zone', 'tags', 'uuid']
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)
