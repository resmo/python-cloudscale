import sys
import click
from ..util import to_table, to_pretty_json
from .. import Cloudscale, CloudscaleException, CloudscaleApiException

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def subnet(ctx, api_token, verbose):
    try:
        ctx.obj = Cloudscale(api_token)
        ctx.obj.verbose = verbose
    except CloudscaleException as e:
        click.echo(e, err=True)
        sys.exit(1)

@subnet.command("list")
@click.pass_obj
def cmd_list(cloudscale):
    try:
        response = cloudscale.subnet.get_all()
        if response:
            headers = ['uuid', 'cidr', 'network', 'tags']
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)


@click.option('--uuid', required=True)
@subnet.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    try:
        response = cloudscale.subnet.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)
