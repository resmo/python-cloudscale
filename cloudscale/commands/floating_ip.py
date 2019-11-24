import sys
import click
from ..util import to_table, to_pretty_json, to_dict
from .. import Cloudscale, CloudscaleApiException, CloudscaleException

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def floating_ip(ctx, api_token, verbose):
    try:
        ctx.obj = Cloudscale(api_token)
        ctx.obj.verbose = verbose
    except CloudscaleException as e:
        click.echo(e, err=True)
        sys.exit(1)

@floating_ip.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    try:
        response = cloudscale.floating_ip.get_all()
        if response:
            headers = ['network', 'ip_version', 'server', 'reverse_ptr', 'region', 'tags']
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--network-id', 'uuid', required=True)
@floating_ip.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    try:
        response = cloudscale.floating_ip.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--ip-version', default=4, show_default=True)
@click.option('--server-uuid', '--server', required=True)
@click.option('--prefix-length', default=32, show_default=True)
@click.option('--reverse-ptr')
@click.option('--region')
@click.option('--tags')
@floating_ip.command("create")
@click.pass_obj
def cmd_create(cloudscale, ip_version, server_uuid, prefix_length, reverse_ptr, region, tags):
    try:
        response = cloudscale.floating_ip.create(
            ip_version=ip_version,
            server_uuid=server_uuid,
            prefix_length=prefix_length,
            reverse_ptr=reverse_ptr,
            region=region,
            tags=to_dict(tags),
        )
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--network-id', 'uuid', required=True)
@click.option('--server-uuid', '--server')
@click.option('--reverse-ptr')
@click.option('--tags')
@floating_ip.command("update")
@click.pass_obj
def cmd_update(cloudscale, uuid, server_uuid, reverse_ptr, tags):
    try:
        cloudscale.floating_ip.update(
            uuid=uuid,
            server_uuid=server_uuid,
            reverse_ptr=reverse_ptr,
            tags=to_dict(tags),
        )
        response = cloudscale.floating_ip.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--network-id', 'uuid', required=True)
@floating_ip.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid):
    try:
        cloudscale.floating_ip.delete(uuid)
        click.echo("Deleted!")
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)
