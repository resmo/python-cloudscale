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
def objects_user(ctx, profile, api_token):
    try:
        ctx.obj = Cloudscale(api_token, profile)
    except CloudscaleException as e:
        logger.error(e)
        sys.exit(1)

@click.option('--filter-tag')
@objects_user.command("list")
@click.pass_obj
def cmd_list(cloudscale, filter_tag):
    try:
        response = cloudscale.objects_user.get_all(filter_tag)
        if response:
            headers = ['display_name', 'id', 'tags']
            table = to_table(response, headers)
            click.echo(table)
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)

@click.option('--id', '--uuid', 'uuid', required=True)
@objects_user.command("show")
@click.pass_obj
def cmd_show(cloudscale, uuid):
    try:
        response = cloudscale.objects_user.get_by_uuid(uuid)
        click.echo(to_pretty_json(response))
    except CloudscaleApiException as e:
        logger.error(e)
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
        logger.error(e)
        sys.exit(1)

@click.option('--id', '--uuid', 'uuid', required=True)
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
        logger.error(e)
        sys.exit(1)

@click.option('--id', '--uuid', 'uuid', required=True)
@click.option('--force', '-f', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Delete?')
@objects_user.command("delete")
@click.pass_obj
def cmd_delete(cloudscale, uuid):
    try:
        cloudscale.objects_user.delete(uuid)
        click.echo("Deleted!")
    except CloudscaleApiException as e:
        logger.error(e)
        sys.exit(1)
