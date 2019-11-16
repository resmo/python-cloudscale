import click
from .. import Cloudscale
from ..util import to_table

@click.group()
@click.option('--api-key', '-a', envvar='CLOUDSCALE_TOKEN')
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def region(ctx, api_key, verbose):
    ctx.obj = Cloudscale(api_key)
    ctx.obj.verbose = verbose

@region.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    results = cloudscale.region.get_all()
    headers = ['zones', 'slug']
    table = to_table(results.get('data'), headers)
    click.echo(table)
