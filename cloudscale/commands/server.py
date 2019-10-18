import click
from .. import Cloudscale

@click.group()
@click.option('--api-key', '-a', envvar='CLOUDSCALE_TOKEN')
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def server(ctx, api_key, verbose):
    ctx.obj = Cloudscale(api_key)
    ctx.obj.verbose = verbose

@server.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    results = cloudscale.server.get_all()
    click.echo(results)

@click.option('--uuid', required=True)
@server.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    results = cloudscale.server.get_by_uuid(uuid)
    click.echo(results)

@server.command("create")
def cmd_create():
    pass
    # results = client.list_resources('servers')
    # click.echo(results)

@server.command("update")
def cmd_update():
    pass

@server.command("delete")
def cmd_delete():
    pass
    # results = client.list_resources('servers')
    # click.echo(results)

@server.command("start")
def cmd_start():
    pass

@server.command("stop")
def cmd_stop():
    pass
