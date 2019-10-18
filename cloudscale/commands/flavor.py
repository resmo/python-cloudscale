import click
from .. import Cloudscale
from ..util import to_table

@click.group()
@click.option('--api-key', '-a', envvar='CLOUDSCALE_TOKEN')
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def flavor(ctx, api_key, verbose):
    ctx.obj = Cloudscale(api_key)
    ctx.obj.verbose = verbose

@flavor.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    results = cloudscale.flavor.get_all()
    headers = ['name', 'vcpu_count', 'memory_gb', 'slug']
    table = to_table(results.get('data'), headers)
    click.echo(table)
