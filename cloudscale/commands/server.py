import sys
import click
from ..util import to_table, to_pretty_json, to_dict
from .. import Cloudscale, CloudscaleApiException, CloudscaleException

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', envvar='CLOUDSCALE_PROFILE', help="Profile used in config file.")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def server(ctx, profile, api_token, verbose):
    try:
        ctx.obj = Cloudscale(api_token, profile, verbose)
    except CloudscaleException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--filter-tag')
@server.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    try:
        response = cloudscale.server.get_all(filter_tag)
        if response:
            headers = ['name', 'flavor', 'zone', 'tags', 'uuid', 'status']
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--uuid', required=True)
@server.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    try:
        response = cloudscale.server.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--name', required=True)
@click.option('--flavor', required=True)
@click.option('--image', required=True)
@click.option('--zone')
@click.option('--volume-size', type=int)
@click.option('--volumes', multiple=True)
@click.option('--interfaces', multiple=True)
@click.option('--ssh-keys', multiple=True)
@click.option('--password')
@click.option('--use-public-network', is_flag=True, default=True)
@click.option('--use-private-network', is_flag=True)
@click.option('--use-ipv6', is_flag=True)
@click.option('--server-groups', multiple=True)
@click.option('--user-data')
@click.option('--tags', multiple=True)
@server.command("create")
@click.pass_obj
def cmd_create(
    cloudscale,
    name,
    flavor,
    image,
    zone,
    volume_size,
    volumes,
    interfaces,
    ssh_keys,
    password,
    use_public_network,
    use_private_network,
    use_ipv6,
    server_groups,
    user_data,
    tags,
):
    try:
        response = cloudscale.server.create(
            name=name,
            flavor=flavor,
            image=image,
            zone=zone,
            volume_size=volume_size,
            volumes=volumes or None,
            interfaces=interfaces or None,
            ssh_keys=ssh_keys or None,
            password=password,
            use_public_network=use_public_network,
            use_private_network=use_private_network,
            use_ipv6=use_ipv6,
            server_groups=server_groups or None,
            user_data=user_data,
            tags=to_dict(tags),
        )
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)


@click.option('--uuid', required=True)
@click.option('--name')
@click.option('--flavor')
@click.option('--tags', multiple=True)
@server.command("update")
@click.pass_obj
def cmd_update(cloudscale, uuid, name, flavor, tags):
    try:
        cloudscale.server.update(
            uuid=uuid,
            name=name,
            flavor=flavor,
            tags=to_dict(tags),
        )
        response = cloudscale.server.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--uuid', required=True)
@server.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid):
    try:
        cloudscale.server.delete(uuid)
        click.echo("Deleted!")
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--uuid', required=True)
@server.command("start")
@click.pass_obj
def cmd_start(cloudscale, uuid):
    try:
        cloudscale.server.start(uuid)
        response = cloudscale.server.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--uuid', required=True)
@server.command("stop")
@click.pass_obj
def cmd_stop(cloudscale, uuid):
    try:
        cloudscale.server.stop(uuid)
        response = cloudscale.server.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--uuid', required=True)
@server.command("reboot")
@click.pass_obj
def cmd_reboot(cloudscale, uuid):
    try:
        cloudscale.server.reboot(uuid)
        response = cloudscale.server.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)
