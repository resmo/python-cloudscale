import click
from . import _init, _list, _show, _create, _update, _delete

headers = ['name', 'type', 'size_gb', 'zone', 'tags', 'uuid']

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', envvar='CLOUDSCALE_PROFILE', help="Profile used in config file.")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def volume(ctx, profile, api_token, verbose):
    _init(
        ctx=ctx,
        api_token=api_token,
        profile=profile,
        verbose=verbose,
    )

@click.option('--filter-tag')
@volume.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    resource = cloudscale.volume
    _list(
        resource=resource,
        headers=headers,
        filter_tag=filter_tag,
    )


@click.argument('uuid', required=True)
@volume.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    resource = cloudscale.volume
    _show(
        resource=resource,
        uuid=uuid,
    )

@click.option('--name', required=True)
@click.option('--server-uuids', multiple=True, required=True)
@click.option('--size-gb', type=int, required=True)
@click.option('--type', 'volume_type', type=click.Choice(['ssd', 'bulk']), default='ssd', show_default=True)
@click.option('--zone')
@click.option('--tag', 'tags', multiple=True)
@volume.command("create")
@click.pass_obj
def cmd_create(cloudscale, name, server_uuids, size_gb, volume_type, zone, tags):
    resource = cloudscale.volume
    _create(
        resource=resource,
        name=name,
        server_uuids=server_uuids,
        size_gb=size_gb,
        volume_type=volume_type,
        zone=zone,
        tags=tags,
    )

@click.argument('uuid', required=True)
@click.option('--name')
@click.option('--server-uuids', multiple=True)
@click.option('--size-gb', type=int)
@click.option('--tag', 'tags', multiple=True)
@click.option('--clear-tag', 'clear_tags', multiple=True)
@click.option('--clear-all-tags', is_flag=True)
@volume.command("update")
@click.pass_obj
def cmd_update(cloudscale, uuid, name, server_uuids, size_gb, tags, clear_tags, clear_all_tags):
    resource = cloudscale.volume
    _update(
        resource=resource,
        uuid=uuid,
        tags=tags,
        clear_tags=clear_tags,
        clear_all_tags=clear_all_tags,
        name=name,
        server_uuids=server_uuids,
        size_gb=size_gb,
    )

@click.argument('uuid', required=True)
@click.option('--force', is_flag=True)
@volume.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid, force):
    resource = cloudscale.volume
    _delete(
        resource=resource,
        uuid=uuid,
        headers=headers,
        force=force,
    )
