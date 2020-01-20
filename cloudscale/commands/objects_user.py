import sys
import click
from ..util import to_table, to_pretty_json, to_dict
from .. import Cloudscale, CloudscaleApiException, CloudscaleException

headers = ['display_name', 'id', 'tags']

@click.group()
@click.option('--api-token', '-a', envvar='CLOUDSCALE_API_TOKEN', help="API token.")
@click.option('--profile', '-p', help="Profile used in config file.")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def objects_user(ctx, profile, api_token, verbose):
    try:
        ctx.obj = Cloudscale(api_token, profile, verbose)
    except CloudscaleException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--filter-tag')
@objects_user.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    try:
        response = cloudscale.objects_user.get_all(filter_tag)
        if response:
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.argument('uuid', required=True)
@objects_user.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    try:
        response = cloudscale.objects_user.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.option('--display-name', required=True)
@click.option('--tags', multiple=True)
@objects_user.command("create")
@click.pass_obj
def cmd_create(cloudscale, display_name, tags):
    try:
        response = cloudscale.objects_user.create(display_name, to_dict(tags))
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.argument('uuid', required=True)
@click.option('--display-name')
@click.option('--tags', multiple=True)
@objects_user.command("update")
@click.pass_obj
def cmd_update(cloudscale, uuid, display_name, tags):
    try:
        cloudscale.objects_user.update(uuid, display_name, to_dict(tags))
        response = cloudscale.objects_user.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)

@click.argument('uuid', required=True)
@click.option('--force', is_flag=True)
@objects_user.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid, force):
    try:
        response = cloudscale.objects_user.get_by_uuid(uuid)
        table = to_table([response], headers)
        click.echo(table)
        if not force:
            click.confirm('Do you want to delete?', abort=True)
        cloudscale.objects_user.delete(uuid)
        click.echo("Deleted!")
    except CloudscaleApiException as e:
        click.echo(e, err=True)
        sys.exit(1)
