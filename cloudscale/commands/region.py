import sys
import click
from ..util import to_table
from .. import Cloudscale, CloudscaleApiException, CloudscaleException
from . import _init, _list

headers = ['zones', 'slug']

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', help="Profile used in config file.")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def region(ctx, profile, api_token, verbose):
    _init(
        ctx=ctx,
        api_token=api_token,
        profile=profile,
        verbose=verbose,
    )

@region.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    resource = cloudscale.region
    _list(
        resource=resource,
        headers=headers,
    )
