import click
from . import _init, _list, _show, _create, _update, _delete

headers = ['network', 'ip_version', 'server', 'reverse_ptr', 'type', 'region', 'tags']

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', help="Profile used in config file.")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def floating_ip(ctx, profile, api_token, verbose):
    _init(
        ctx=ctx,
        api_token=api_token,
        profile=profile,
        verbose=verbose,
    )

@click.option('--filter-tag')
@floating_ip.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    resource = cloudscale.floating_ip
    _list(
        resource=resource,
        headers=headers,
        filter_tag=filter_tag,
    )

@click.argument('network-id', required=True)
@floating_ip.command("show")
@click.pass_obj
def cmd_show(cloudscale, network_id):
    resource = cloudscale.floating_ip
    _show(
        resource=resource,
        uuid=network_id,
    )

@click.option('--ip-version', type=int, default=4, show_default=True)
@click.option('--server-uuid', '--server', required=True)
@click.option('--prefix-length', type=int, show_default=True)
@click.option('--reverse-ptr')
@click.option('--type', 'scope', type=click.Choice(['regional', 'global']), default='regional', show_default=True)
@click.option('--region')
@click.option('--tag', 'tags', multiple=True)
@floating_ip.command("create")
@click.pass_obj
def cmd_create(cloudscale, ip_version, server_uuid, prefix_length, reverse_ptr, scope, region, tags):
    if not prefix_length:
        if ip_version == 6:
            prefix_length = 128
        else:
            prefix_length = 32

    resource = cloudscale.floating_ip
    _create(
        resource=resource,
        ip_version=ip_version,
        server_uuid=server_uuid,
        prefix_length=prefix_length,
        reverse_ptr=reverse_ptr,
        scope=scope,
        region=region,
        tags=tags,
    )

@click.argument('network-id', required=True)
@click.option('--server-uuid', '--server')
@click.option('--reverse-ptr')
@click.option('--tag', 'tags', multiple=True)
@click.option('--clear-tag', 'clear_tags', multiple=True)
@click.option('--clear-all-tags', is_flag=True)
@floating_ip.command("update")
@click.pass_obj
def cmd_update(cloudscale, network_id, server_uuid, reverse_ptr, tags, clear_tags, clear_all_tags):
    resource = cloudscale.floating_ip
    _update(
        resource=resource,
        uuid=network_id,
        tags=tags,
        clear_tags=clear_tags,
        clear_all_tags=clear_all_tags,
        server_uuid=server_uuid,
        reverse_ptr=reverse_ptr,
    )

@click.argument('network-id', required=True)
@click.option('--force', is_flag=True)
@floating_ip.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, network_id, force):
    resource = cloudscale.floating_ip
    _delete(
        resource=resource,
        uuid=network_id,
        headers=headers,
        force=force,
    )
