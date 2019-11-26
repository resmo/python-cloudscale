import sys
import click
from ..util import to_table
from .. import Cloudscale, CloudscaleException, CloudscaleApiException

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def flavor(ctx, api_token, verbose):
    try:
        ctx.obj = Cloudscale(api_token)
        ctx.obj.verbose = verbose
    except CloudscaleException as e:
        click.echo(e, err=True)
        sys.exit(1)

@flavor.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    try:
        response = cloudscale.flavor.get_all()
        if response:
            headers = ['name', 'vcpu_count', 'memory_gb', 'slug']
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)
