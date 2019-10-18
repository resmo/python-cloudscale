import click
from ..util import to_table
from .. import Cloudscale

@click.group()
@click.option('--api-key', '-a', envvar='CLOUDSCALE_TOKEN')
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def image(ctx, api_key, verbose):
    ctx.obj = Cloudscale(api_key)
    ctx.obj.verbose = verbose

@image.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    results = cloudscale.image.get_all()
    headers = ['name', 'operating_system', 'default_username', 'slug']
    table = to_table(results.get('data'), headers)
    click.echo(table)
