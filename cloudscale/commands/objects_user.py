import click
from . import _init, _list, _show, _create, _update, _delete

headers = ['display_name', 'id', 'tags']

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', help="Profile used in config file.")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def objects_user(ctx, profile, api_token, verbose):
    _init(
        ctx=ctx,
        api_token=api_token,
        profile=profile,
        verbose=verbose,
    )

@click.option('--filter-tag')
@objects_user.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    resource = cloudscale.objects_user
    _list(
        resource=resource,
        headers=headers,
        filter_tag=filter_tag,
    )

@click.argument('uuid', required=True)
@objects_user.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    resource = cloudscale.objects_user
    _show(
        resource=resource,
        uuid=uuid,
    )

@click.option('--display-name', required=True)
@click.option('--tag', 'tags', multiple=True)
@objects_user.command("create")
@click.pass_obj
def cmd_create(cloudscale, display_name, tags):
    resource = cloudscale.objects_user
    _create(
        resource=resource,
        display_name=display_name,
        tags=tags
    )

@click.argument('uuid', required=True)
@click.option('--display-name')
@click.option('--tag', 'tags', multiple=True)
@click.option('--clear-tag', 'clear_tags', multiple=True)
@click.option('--clear-all-tags', is_flag=True)
@objects_user.command("update")
@click.pass_obj
def cmd_update(cloudscale, uuid, display_name, tags, clear_tags, clear_all_tags):
    resource = cloudscale.objects_user
    _update(
        resource=resource,
        uuid=uuid,
        tags=tags,
        clear_tags=clear_tags,
        clear_all_tags=clear_all_tags,
        display_name=display_name
    )

@click.argument('uuid', required=True)
@click.option('--force', is_flag=True)
@objects_user.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid, force):
    resource = cloudscale.objects_user
    _delete(
        resource=resource,
        uuid=uuid,
        headers=headers,
        force=force,
    )
