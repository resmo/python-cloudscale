from cloudscale import Cloudscale, CloudscaleApiException, CloudscaleException, CLOUDSCALE_API_ENDPOINT
from cloudscale.cli import cli
import responses
import click
from click.testing import CliRunner

SERVER_GROUP_RESP = {
    "href": "https://api.cloudscale.ch/v1/server-groups/e3b63018-fad6-45f2-9f57-3ea0da726d8c",
    "uuid": "e3b63018-fad6-45f2-9f57-3ea0da726d8c",
    "name": "load balancers",
    "type": "anti-affinity",
    "servers": [
        {
            "href": "https://api.cloudscale.ch/v1/server-groups/32d2f586-14ff-4da9-81df-134ca45d635f",
            "uuid": "32d2f586-14ff-4da9-81df-134ca45d635f",
            "name": "tesla"
        },
        {
            "href": "https://api.cloudscale.ch/v1/server-groups/375870c2-d4ee-49af-a048-efcf59ef14ef",
            "uuid": "375870c2-d4ee-49af-a048-efcf59ef14ef",
            "name": "edison"
        }
    ],
    "zone": {
        "slug": "rma1"
    },
    "tags": {}
}

@responses.activate
def test_server_groups_get_all():
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/server-groups',
        json=[SERVER_GROUP_RESP],
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/server-groups',
        json=[SERVER_GROUP_RESP],
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/server-groups',
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    server_groups = cloudscale.server_group.get_all()
    assert server_groups[0]['name'] == "load balancers"
    assert server_groups[0]['uuid'] == "e3b63018-fad6-45f2-9f57-3ea0da726d8c"

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server-group',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'server-group',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code > 0

@responses.activate
def test_server_groups_get_by_uuid():
    uuid = "e3b63018-fad6-45f2-9f57-3ea0da726d8c"
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/' + uuid,
        json=SERVER_GROUP_RESP,
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/' + uuid,
        json=SERVER_GROUP_RESP,
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/' + uuid,
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    server_group = cloudscale.server_group.get_by_uuid(uuid=uuid)
    assert server_group['name'] == "load balancers"
    assert server_group['uuid'] == uuid

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'show',
        uuid,
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'show',
        uuid,
    ])
    assert result.exit_code > 0

@responses.activate
def test_server_groups_delete():
    uuid = "e3b63018-fad6-45f2-9f57-3ea0da726d8c"
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/' + uuid,
        json=SERVER_GROUP_RESP,
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/unknown',
        json=SERVER_GROUP_RESP,
        status=200)
    responses.add(
        responses.DELETE,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/' + uuid,
        status=204)
    responses.add(
        responses.DELETE,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/unknown',
        json={
            "detail": "Not found."
        },
        status=404)

    cloudscale = Cloudscale(api_token="token")
    server_group = cloudscale.server_group.delete(uuid=uuid)
    assert server_group is None

    try:
        cloudscale = Cloudscale(api_token="token")
        cloudscale.server_group.delete(uuid="unknown")
    except CloudscaleApiException as e:
        assert e.status_code == 404

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'delete',
        uuid,
    ])
    assert result.exit_code == 1
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'delete',
        '--force',
        uuid,
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'delete',
        '--force',
        'unknown',
    ])
    assert result.exit_code > 0

@responses.activate
def test_server_groups_create():
    name = "load balancers"
    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/server-groups',
        json=SERVER_GROUP_RESP,
        status=201)
    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/server-groups',
        json=SERVER_GROUP_RESP,
        status=201)
    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/server-groups',
        json=SERVER_GROUP_RESP,
        status=500)

    cloudscale = Cloudscale(api_token="token")
    cloudscale.server_group.create(
        name=name,
    )
    runner = CliRunner()
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'create',
        '--name',
        name,
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'create',
        '--name',
        name,
    ])
    assert result.exit_code > 0

@responses.activate
def test_server_groups_update():
    uuid = "e3b63018-fad6-45f2-9f57-3ea0da726d8c"
    name = "load balancers"
    responses.add(
        responses.PATCH,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/' + uuid,
        json=SERVER_GROUP_RESP,
        status=204)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/' + uuid,
        json=SERVER_GROUP_RESP,
        status=200)
    responses.add(
        responses.PATCH,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/' + uuid,
        json=SERVER_GROUP_RESP,
        status=204)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/' + uuid,
        json=SERVER_GROUP_RESP,
        status=200)
    responses.add(
        responses.PATCH,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/' + uuid,
        json={},
        status=500)
    cloudscale = Cloudscale(api_token="token")
    server_group = cloudscale.server_group.update(uuid=uuid, name=name)
    assert server_group['name'] == name
    assert server_group['uuid'] == uuid

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'update',
        '--name',
        name,
        uuid,
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'update',
        '--name',
        name,
        '--clear-tag',
        'foo',
        uuid,
    ])
    assert result.exit_code > 0

@responses.activate
def test_server_group_get_by_uuid_not_found():
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/unknown',
        json={
            "detail": "Not found."
        },
        status=404)
    try:
        cloudscale = Cloudscale(api_token="token")
        cloudscale.server_group.get_by_uuid(uuid="unknown")
    except CloudscaleApiException as e:
        assert e.status_code == 404
        assert str(e) == "API Response Error (404): Not found."
        assert e.response == {'data': {'detail': 'Not found.'}, 'status_code': 404}

def test_server_group_missing_api_key():
    runner = CliRunner()
    result = runner.invoke(cli, [
        'server-group',
        'list',
    ])
    assert result.exit_code == 1

@responses.activate
def test_invalid_tags_create():
    name = "load balancers"
    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/server-groups',
        json=SERVER_GROUP_RESP,
        status=201)

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'create',
        '--name',
        name,
        '--tag',
        'foo',
    ])
    assert result.exit_code == 1

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'create',
        '--name',
        name,
        '--tag',
        'foo=',
    ])
    assert result.exit_code == 0

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'create',
        '--name',
        name,
        '--tag',
        'foo=bar=',
    ])
    assert result.exit_code == 0


@responses.activate
def test_invalid_tags_update():
    uuid = "e3b63018-fad6-45f2-9f57-3ea0da726d8c"
    name = "load balancers"
    responses.add(
        responses.PATCH,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/' + uuid,
        json=SERVER_GROUP_RESP,
        status=204)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/server-groups/' + uuid,
        json=SERVER_GROUP_RESP,
        status=200)

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'update',
        '--name',
        name,
        uuid,
        '--tag',
        'foo',
    ])
    assert result.exit_code == 1

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'update',
        '--name',
        name,
        uuid,
        '--tag',
        'foo=',
    ])
    assert result.exit_code == 0

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server-group',
        '-a', 'token',
        'update',
        '--name',
        name,
        uuid,
        '--tag',
        'foo=bar=',
    ])
    assert result.exit_code == 0
