import click
from . import _init, _list, _show, _create, _update, _delete

headers = ['uuid', 'cidr', 'network', 'tags']

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', envvar='CLOUDSCALE_PROFILE', help="Profile used in config file.")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def subnet(ctx, profile, api_token, verbose):
    _init(
        ctx=ctx,
        api_token=api_token,
        profile=profile,
        verbose=verbose,
    )

@click.option('--filter-tag')
@subnet.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    resource = cloudscale.subnet
    _list(
        resource=resource,
        headers=headers,
        filter_tag=filter_tag,
    )

@click.argument('uuid', required=True)
@subnet.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    resource = cloudscale.subnet
    _show(
        resource=resource,
        uuid=uuid,
    )
