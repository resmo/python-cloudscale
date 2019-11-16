import click
from .. import Cloudscale
from ..util import to_table

@click.group()
@click.option('--api-key', '-a', envvar='CLOUDSCALE_TOKEN')
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def network(ctx, api_key, verbose):
    ctx.obj = Cloudscale(api_key)
    ctx.obj.verbose = verbose

@network.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    results = cloudscale.network.get_all()
    headers = ['name', 'created_at', 'zone', 'tags', 'uuid']
    table = to_table(results.get('data'), headers)
    click.echo(table)
