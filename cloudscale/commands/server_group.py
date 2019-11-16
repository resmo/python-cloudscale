import click
from .. import Cloudscale
from ..util import to_table, to_pretty_json, to_dict

@click.group()
@click.option('--api-key', '-a', envvar='CLOUDSCALE_TOKEN')
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def server_group(ctx, api_key, verbose):
    ctx.obj = Cloudscale(api_key)
    ctx.obj.verbose = verbose

@click.option('--filter-tag')
@server_group.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    results = cloudscale.server_group.get_all(filter_tag)
    headers = ['name', 'type', 'servers', 'tags', 'uuid']
    table = to_table(results.get('data'), headers)
    click.echo(table)

@click.option('--uuid', required=True)
@server_group.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    results = cloudscale.server_group.get_by_uuid(uuid)
    click.echo(to_pretty_json(results))

@click.option('--name', required=True)
@click.option('--type', 'group_type', default='anti-affinity', show_default=True)
@click.option('--tags', multiple=True)
@server_group.command("create")
@click.pass_obj
def cmd_create(cloudscale, name, group_type, tags):
    results = cloudscale.server_group.create(name, group_type, to_dict(tags))
    click.echo(to_pretty_json(results))

@click.option('--uuid', required=True)
@click.option('--name')
@click.option('--tags', multiple=True)
@server_group.command("update")
@click.pass_obj
def cmd_update(cloudscale, uuid, name, tags):
    results = cloudscale.server_group.update(uuid, name, to_dict(tags))
    click.echo(to_pretty_json(results))

@click.option('--uuid', required=True)
@server_group.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid):
    results = cloudscale.server_group.delete(uuid)
    click.echo(to_pretty_json(results))
