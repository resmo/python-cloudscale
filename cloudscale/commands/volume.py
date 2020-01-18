import sys
import click
from ..log import logger
from ..util import to_table, to_pretty_json, to_dict
from .. import Cloudscale, CloudscaleApiException, CloudscaleException
from . import abort_if_false

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', envvar='CLOUDSCALE_PROFILE', help="Profile used in config file.")
@click.pass_context
def volume(ctx, profile, api_token):
    try:
        ctx.obj = Cloudscale(api_token, profile)
    except CloudscaleException as e:
        logger.error(e)
        sys.exit(1)

@click.option('--filter-tag')
@volume.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    try:
        response = cloudscale.volume.get_all(filter_tag)
        if response:
            headers = ['name', 'type', 'size_gb', 'zone', 'tags', 'uuid']
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)

@click.option('--uuid', required=True)
@volume.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    try:
        response = cloudscale.volume.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)

@click.option('--name', required=True)
@click.option('--server-uuids', multiple=True, required=True)
@click.option('--size-gb', type=int, required=True)
@click.option('--type', 'volume_type', type=click.Choice(['ssd', 'bulk']), default='ssd', show_default=True)
@click.option('--zone')
@click.option('--tags', multiple=True)
@volume.command("create")
@click.pass_obj
def cmd_create(cloudscale, name, server_uuids, size_gb, volume_type, zone, tags):
    try:
        response = cloudscale.volume.create(
            name=name,
            server_uuids=server_uuids,
            size_gb=size_gb,
            volume_type=volume_type,
            zone=zone,
            tags=to_dict(tags),
        )
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)

@click.option('--uuid', required=True)
@click.option('--name')
@click.option('--server-uuids', multiple=True)
@click.option('--size-gb', type=int)
@click.option('--tags', multiple=True)
@volume.command("update")
@click.pass_obj
def cmd_update(cloudscale, uuid, name, server_uuids, size_gb, tags):
    try:
        cloudscale.volume.update(
            uuid=uuid,
            name=name,
            server_uuids=server_uuids,
            size_gb=size_gb,
            tags=to_dict(tags),
        )
        response = cloudscale.volume.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)

@click.option('--uuid', required=True)
@click.option('--force', '-f', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Delete?')
@volume.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid):
    try:
        cloudscale.volume.delete(uuid)
        click.echo("Deleted!")
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)
