import click
from . import _init, _list, _show, _create, _update, _delete

headers = ['name', 'created_at', 'zone', 'tags', 'uuid']

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', help="Profile used in config file.")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def network(ctx, profile, api_token, verbose):
    _init(
        ctx=ctx,
        api_token=api_token,
        profile=profile,
        verbose=verbose,
    )

@click.option('--filter-tag')
@network.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    resource = cloudscale.network
    _list(
        resource=resource,
        headers=headers,
        filter_tag=filter_tag,
    )

@click.argument('uuid', required=True)
@network.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    resource = cloudscale.network
    _show(
        resource=resource,
        uuid=uuid,
    )

@click.option('--name', required=True)
@click.option('--zone')
@click.option('--mtu', type=int, default=9000)
@click.option('--auto-create-ipv4-subnet', type=bool, default=True)
@click.option('--tag', 'tags', multiple=True)
@network.command("create")
@click.pass_obj
def cmd_create(cloudscale, name, zone, mtu, auto_create_ipv4_subnet, tags):
    resource = cloudscale.network
    _create(
        resource=resource,
        name=name,
        zone=zone,
        mtu=mtu,
        auto_create_ipv4_subnet=auto_create_ipv4_subnet,
        tags=tags,
        )

@click.argument('uuid', required=True)
@click.option('--name')
@click.option('--mtu', type=int)
@click.option('--tag', 'tags', multiple=True)
@click.option('--clear-tag', 'clear_tags', multiple=True)
@click.option('--clear-all-tags', is_flag=True)
@network.command("update")
@click.pass_obj
def cmd_update(cloudscale, uuid, name, mtu, tags, clear_tags, clear_all_tags):
    resource = cloudscale.network
    _update(
        resource=resource,
        uuid=uuid,
        tags=tags,
        clear_tags=clear_tags,
        clear_all_tags=clear_all_tags,
        name=name,
        mtu=mtu,
    )

@click.argument('uuid', required=True)
@click.option('--force', is_flag=True)
@network.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid, force):
    resource = cloudscale.network
    _delete(
        resource=resource,
        uuid=uuid,
        headers=headers,
        force=force,
    )
