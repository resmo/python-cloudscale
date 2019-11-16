import click
from .. import Cloudscale
from ..util import to_table, to_pretty_json, to_dict

@click.group()
@click.option('--api-key', '-a', envvar='CLOUDSCALE_TOKEN')
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def server(ctx, api_key, verbose):
    ctx.obj = Cloudscale(api_key)
    ctx.obj.verbose = verbose

@click.option('--filter-tag')
@server.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    results = cloudscale.server.get_all(filter_tag)
    headers = ['name', 'flavor', 'zone', 'tags', 'uuid']
    table = to_table(results.get('data'), headers)
    click.echo(table)

@click.option('--uuid', required=True)
@server.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    results = cloudscale.server.get_by_uuid(uuid)
    click.echo(results)

@click.option('--name', required=True)
@click.option('--flavor', required=True)
@click.option('--image', required=True)
@click.option('--zone')
@click.option('--volume-size', type=int)
@click.option('--volumes', multiple=True)
@click.option('--interfaces', multiple=True)
@click.option('--ssh-keys', multiple=True)
@click.option('--password')
@click.option('--use-public-network', is_flag=True, default=True)
@click.option('--use-private-network', is_flag=True)
@click.option('--use-ipv6', is_flag=True)
@click.option('--server-groups', multiple=True)
@click.option('--user-data')
@click.option('--tags', multiple=True)
@server.command("create")
@click.pass_obj
def cmd_create(
    cloudscale,
    name,
    flavor,
    image,
    zone,
    volume_size,
    volumes,
    interfaces,
    ssh_keys,
    password,
    use_public_network,
    use_private_network,
    use_ipv6,
    server_groups,
    user_data,
    tags,
    ):
    results = cloudscale.server.create(
        name=name,
        flavor=flavor,
        image=image,
        zone=zone,
        volume_size=volume_size,
        volumes=volumes or None,
        interfaces=interfaces or None,
        ssh_keys=ssh_keys or None,
        password=password,
        use_public_network=use_public_network,
        use_private_network=use_private_network,
        use_ipv6=use_ipv6,
        server_groups=server_groups or None,
        user_data=user_data,
        tags=to_dict(tags),
    )
    click.echo(results)

@click.option('--uuid', required=True)
@server.command("update")
@click.pass_obj
def cmd_update(cloudscale, uuid):
    results = cloudscale.server.update(
        uuid=uuid,
        name=name,
        flavor=flavor,
        interfaces=interfaces,
        tags=tags,
    )
    click.echo(results)

@click.option('--uuid', required=True)
@server.command("delete")
@click.pass_obj
def cmd_create(cloudscale, uuid):
    results = cloudscale.server.delete(uuid)
    click.echo(results)

@click.option('--uuid', required=True)
@server.command("start")
@click.pass_obj
def cmd_start(cloudscale, uuid):
    results = cloudscale.server.start(uuid)
    click.echo(results)

@click.option('--uuid', required=True)
@server.command("stop")
@click.pass_obj
def cmd_stop(cloudscale, uuid):
    results = cloudscale.server.stop(uuid)
    click.echo(results)
