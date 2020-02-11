import click
from . import _init, _list, _show, _create, _update, _delete, _act

headers = ['name', 'image', 'flavor', 'zone', 'tags', 'server_groups', 'uuid', 'status']

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', help="Profile used in config file.")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def server(ctx, profile, api_token, verbose):
    _init(
        ctx=ctx,
        api_token=api_token,
        profile=profile,
        verbose=verbose,
    )

@click.option('--filter-tag')
@server.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    resource = cloudscale.server
    _list(
        resource=resource,
        headers=headers,
        filter_tag=filter_tag,
    )

@click.argument('uuid', required=True)
@server.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    resource = cloudscale.server
    _show(
        resource=resource,
        uuid=uuid,
    )

@click.option('--name', required=True)
@click.option('--flavor', required=True)
@click.option('--image', required=True)
@click.option('--zone')
@click.option('--volume-size', type=int, default=10)
@click.option('--volume', 'volumes', multiple=True)
@click.option('--interface', 'interfaces', multiple=True)
@click.option('--ssh-key', 'ssh_keys', multiple=True)
@click.option('--password')
@click.option('--use-public-network/--no-use-public-network', default=True)
@click.option('--use-private-network/--no-use-private-network', default=False)
@click.option('--use-ipv6/--no-use-ipv6', default=True)
@click.option('--server-group', 'server_groups', multiple=True)
@click.option('--user-data')
@click.option('--tag', 'tags', multiple=True)
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
    resource = cloudscale.server
    _create(
        resource=resource,
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
        tags=tags,
    )

@click.argument('uuid', required=True)
@click.option('--name')
@click.option('--flavor')
@click.option('--interface', 'interfaces', multiple=True)
@click.option('--tag', 'tags', multiple=True)
@click.option('--clear-tag', 'clear_tags', multiple=True)
@click.option('--clear-all-tags', is_flag=True)
@server.command("update")
@click.pass_obj
def cmd_update(cloudscale, uuid, name, flavor, interfaces, tags, clear_tags, clear_all_tags):
    resource = cloudscale.server
    _update(
        resource=resource,
        uuid=uuid,
        tags=tags,
        clear_tags=clear_tags,
        clear_all_tags=clear_all_tags,
        name=name,
        flavor=flavor,
        interfaces=interfaces,
    )

@click.argument('uuid', required=True)
@click.option('--force', is_flag=True)
@server.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid, force):
    resource = cloudscale.server
    _delete(
        resource=resource,
        uuid=uuid,
        headers=headers,
        force=force,
    )

@click.argument('uuid', required=True)
@server.command("start")
@click.pass_obj
def cmd_start(cloudscale, uuid):
    resource = cloudscale.server
    _act(
        resource=resource,
        action="start",
        uuid=uuid,
    )

@click.argument('uuid', required=True)
@server.command("stop")
@click.pass_obj
def cmd_stop(cloudscale, uuid):
    resource = cloudscale.server
    _act(
        resource=resource,
        action="stop",
        uuid=uuid,
    )

@click.argument('uuid', required=True)
@server.command("reboot")
@click.pass_obj
def cmd_reboot(cloudscale, uuid):
    resource = cloudscale.server
    _act(
        resource=resource,
        action="reboot",
        uuid=uuid,
    )
