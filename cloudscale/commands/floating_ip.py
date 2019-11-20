import sys
import click
from ..util import to_table, to_pretty_json
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
        results = cloudscale.floating_ip.get_all()
        data = results.get('data')
        if data:
            headers = ['network', 'created_at', 'ip_version', 'server', 'reverse_ptr', 'href']
            table = to_table(results.get('data'), headers)
            click.echo(table)
    except CloudscaleApiException as e:
        click.echo(to_pretty_json(e.result), err=True)
        sys.exit(1)


@click.option('--network-id', 'uuid', required=True)
@floating_ip.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    try:
        results = cloudscale.floating_ip.get_by_uuid(uuid)
        click.echo(to_pretty_json(results))
    except CloudscaleApiException as e:
        click.echo(to_pretty_json(e.result), err=True)
        sys.exit(1)


@click.option('--ip-version', default=4, show_default=True)
@click.option('--server-uuid', '--server', required=True)
@click.option('--prefix-length', default=32, show_default=True)
@click.option('--reverse-ptr')
@click.option('--tags')
@floating_ip.command("create")
@click.pass_obj
def cmd_create(cloudscale, ip_version, server_uuid, prefix_length, reverse_ptr, tags):
    try:
        results = cloudscale.floating_ip.create(ip_version, server_uuid, prefix_length, reverse_ptr, tags)
        click.echo(to_pretty_json(results))
    except CloudscaleApiException as e:
        click.echo(to_pretty_json(e.result), err=True)
        sys.exit(1)

@click.option('--network-id', 'uuid', required=True)
@floating_ip.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid):
    try:
        results = cloudscale.floating_ip.delete(uuid)
        click.echo(to_pretty_json(results))
    except CloudscaleApiException as e:
        click.echo(to_pretty_json(e.result), err=True)
        sys.exit(1)
