import click
from .. import Cloudscale
from ..util import to_table, to_pretty_json

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
    headers = ['network', 'created_at', 'ip_version', 'server', 'reverse_ptr', 'href']
    table = to_table(results.get('data'), headers)
    click.echo(table)

@click.option('--network-id', 'uuid', required=True)
@floating_ip.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    results = cloudscale.floating_ip.get_by_uuid(uuid)
    click.echo(to_pretty_json(results))

@click.option('--ip-version', default=4, show_default=True)
@click.option('--server-uuid', '--server', required=True)
@click.option('--prefix-length', default=32, show_default=True)
@click.option('--reverse-ptr')
@click.option('--tags')
@floating_ip.command("create")
@click.pass_obj
def cmd_create(cloudscale, ip_version, server_uuid, prefix_length, reverse_ptr, tags):
    results = cloudscale.floating_ip.create(ip_version, server_uuid, prefix_length, reverse_ptr, tags)
    click.echo(to_pretty_json(results))


@click.option('--network-id', 'uuid', required=True)
@floating_ip.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid):
    results = cloudscale.floating_ip.delete(uuid)
    click.echo(to_pretty_json(results))
