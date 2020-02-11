import click
from . import _init, _list, _show, _create, _update, _delete

headers = ['name', 'type', 'servers', 'tags', 'uuid']

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', help="Profile used in config file.")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def server_group(ctx, profile, api_token, verbose):
    _init(
        ctx=ctx,
        api_token=api_token,
        profile=profile,
        verbose=verbose,
    )

@click.option('--filter-tag')
@server_group.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    resource = cloudscale.server_group
    _list(
        resource=resource,
        headers=headers,
        filter_tag=filter_tag,
    )

@click.argument('uuid', required=True)
@server_group.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    resource = cloudscale.server_group
    _show(
        resource=resource,
        uuid=uuid,
    )

@click.option('--name', required=True)
@click.option('--type', 'group_type', default='anti-affinity', show_default=True)
@click.option('--tag', 'tags', multiple=True)
@server_group.command("create")
@click.pass_obj
def cmd_create(cloudscale, name, group_type, tags):
    resource = cloudscale.server_group
    _create(
        resource=resource,
        name=name,
        group_type=group_type,
        tags=tags,
    )

@click.argument('uuid', required=True)
@click.option('--name')
@click.option('--tag', 'tags', multiple=True)
@click.option('--clear-tag', 'clear_tags', multiple=True)
@click.option('--clear-all-tags', is_flag=True)
@server_group.command("update")
@click.pass_obj
def cmd_update(cloudscale, uuid, name, tags, clear_tags, clear_all_tags):
    resource = cloudscale.server_group
    _update(
        resource=resource,
        uuid=uuid,
        tags=tags,
        clear_tags=clear_tags,
        clear_all_tags=clear_all_tags,
        name=name,
    )

@click.argument('uuid', required=True)
@click.option('--force', is_flag=True)
@server_group.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid, force):
    resource = cloudscale.server_group
    _delete(
        resource=resource,
        uuid=uuid,
        headers=headers,
        force=force,
    )
