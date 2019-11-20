import sys
import click
from ..util import to_table, to_pretty_json
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
        results = cloudscale.flavor.get_all()
        data = results.get('data')
        if data:
            headers = ['name', 'vcpu_count', 'memory_gb', 'slug']
            table = to_table(results.get('data'), headers)
            click.echo(table)
    except CloudscaleApiException as e:
        click.echo(to_pretty_json(e.result), err=True)
        sys.exit(1)
