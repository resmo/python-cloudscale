import sys
import click
from ..util import to_table, to_pretty_json
from .. import Cloudscale, CloudscaleApiException, CloudscaleException


@click.group()
@click.option('--api-key', '-a', envvar='CLOUDSCALE_TOKEN')
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def network(ctx, api_key, verbose):
    try:
        ctx.obj = Cloudscale(api_key)
        ctx.obj.verbose = verbose
    except CloudscaleException as e:
        click.echo(e, err=True)
        sys.exit(1)

@network.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    try:
        results = cloudscale.network.get_all()
        data = results.get('data')
        if data:
            headers = ['name', 'created_at', 'zone', 'tags', 'uuid']
            table = to_table(results.get('data'), headers)
            click.echo(table)
    except CloudscaleApiException as e:
        click.echo(to_pretty_json(e.result), err=True)
        sys.exit(1)
