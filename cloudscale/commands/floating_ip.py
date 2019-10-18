import click
from .. import Cloudscale

@click.group()
@click.option('--api-key', '-a', envvar='CLOUDSCALE_TOKEN')
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def floating_ip(ctx, api_key, verbose):
    ctx.obj = Cloudscale(api_key)
    ctx.obj.verbose = verbose

@floating_ip.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    results = cloudscale.floating_ip.get_all()
    click.secho(results)

@click.option('--uuid', required=True)
@floating_ip.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    results = cloudscale.floating_ip.get_by_uuid(uuid)
    click.secho(results)

@click.option('--uuid', required=True)
@floating_ip.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid):
    results = cloudscale.floating_ip.delete(uuid)
    click.secho(results)
