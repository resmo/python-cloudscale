import sys
import click
from ..log import logger
from ..util import to_table, to_pretty_json, to_dict
from .. import Cloudscale, CloudscaleApiException, CloudscaleException
from . import abort_if_false

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', help="Profile used in config file.")
@click.pass_context
def network(ctx, profile, api_token):
    try:
        ctx.obj = Cloudscale(api_token, profile)
    except CloudscaleException as e:
        logger.error(e)
        sys.exit(1)

@network.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    try:
        response = cloudscale.network.get_all()
        if response:
            headers = ['name', 'created_at', 'zone', 'tags', 'uuid']
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)

@click.option('--uuid', required=True)
@network.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    try:
        response = cloudscale.network.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)

@click.option('--name', required=True)
@click.option('--zone')
@click.option('--mtu', type=int, default=9000)
@click.option('--auto-create-ipv4-subnet', type=bool, default=True)
@click.option('--tags', multiple=True)
@network.command("create")
@click.pass_obj
def cmd_create(cloudscale, name, zone, mtu, auto_create_ipv4_subnet, tags):
    try:
        response = cloudscale.network.create(
            name=name,
            zone=zone,
            mtu=mtu,
            auto_create_ipv4_subnet=auto_create_ipv4_subnet,
            tags=to_dict(tags),
        )
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)

@click.option('--uuid', required=True)
@click.option('--name')
@click.option('--mtu', type=int)
@click.option('--tags', multiple=True)
@network.command("update")
@click.pass_obj
def cmd_update(cloudscale, uuid, name, mtu, tags):
    try:
        cloudscale.network.update(
            uuid=uuid,
            name=name,
            mtu=mtu,
            tags=to_dict(tags),
        )
        response = cloudscale.network.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)

@click.option('--uuid', required=True)
@click.option('--force', '-f', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Delete?')
@network.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid):
    try:
        cloudscale.network.delete(uuid)
        click.echo("Deleted!")
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)
