import sys
import click
from ..util import to_table, to_pretty_json, to_dict
from .. import Cloudscale, CloudscaleApiException, CloudscaleException

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def network(ctx, api_token, verbose):
    try:
        ctx.obj = Cloudscale(api_token)
        ctx.obj.verbose = verbose
    except CloudscaleException as e:
        click.echo(e, err=True)
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
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--uuid', required=True)
@network.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    try:
        response = cloudscale.network.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
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
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--uuid', required=True)
@click.option('--name')
@click.option('--mtu')
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
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--uuid', required=True)
@network.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid):
    try:
        cloudscale.network.delete(uuid)
        click.echo("Deleted!")
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)
