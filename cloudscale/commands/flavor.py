import click
from . import _init, _list

headers = ['name', 'vcpu_count', 'memory_gb', 'slug', 'zones']

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', help="Profile used in config file.")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def flavor(ctx, profile, api_token, verbose):
    _init(
        ctx=ctx,
        api_token=api_token,
        profile=profile,
        verbose=verbose,
    )

@flavor.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    resource = cloudscale.flavor
    _list(
        resource=resource,
        headers=headers,
    )
