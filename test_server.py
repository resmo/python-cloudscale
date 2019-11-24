from cloudscale import Cloudscale, CloudscaleApiException, CloudscaleException, CLOUDSCALE_API_ENDPOINT
from cloudscale.cli import cli
import responses
import click
from click.testing import CliRunner

SERVER_RESP = {
    "uuid": "47cec963-fcd2-482f-bdb6-24461b2d47b1",
    "name": "db-master",
    "status": "running",
    "zone": {
        "slug": "lpg1"
    },
    "flavor": {
        "slug": "flex-4",
    },
    "image": {
        "slug": "debian-9",
    },
    "server_groups": [],
    "anti_affinity_with": [],
    "tags": {
        "project": "gemini"
    }
}

@responses.activate
def test_server_get_all():
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/servers',
        json=[SERVER_RESP],
        status=200)

    cloudscale = Cloudscale(api_token="token")
    servers = cloudscale.server.get_all()
    assert servers[0]['name'] == "db-master"
    assert servers[0]['uuid'] == "47cec963-fcd2-482f-bdb6-24461b2d47b1"
    assert servers[0]['tags']['project'] == "gemini"

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code == 0

@responses.activate
def test_server_get_by_uuid():
    uuid = "47cec963-fcd2-482f-bdb6-24461b2d47b1"
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/servers/' + uuid,
        json=SERVER_RESP,
        status=200)

    cloudscale = Cloudscale(api_token="token")
    server = cloudscale.server.get_by_uuid(uuid=uuid)
    assert server['name'] == "db-master"
    assert server['uuid'] == uuid
    assert server['tags']['project'] == "gemini"

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server',
        '-a', 'token',
        'show',
        '--uuid',
        uuid,
    ])
    assert result.exit_code == 0

@responses.activate
def test_server_delete():
    uuid = "47cec963-fcd2-482f-bdb6-24461b2d47b1"

    responses.add(
        responses.DELETE,
        CLOUDSCALE_API_ENDPOINT + '/servers/' + uuid,
        status=204)

    cloudscale = Cloudscale(api_token="token")
    server = cloudscale.server.delete(uuid=uuid)
    assert server is None

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server',
        '-a', 'token',
        'delete',
        '--uuid',
        uuid,
    ])
    assert result.exit_code == 0

@responses.activate
def test_server_get_by_uuid_not_found():
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/servers/unknown',
        json={
            "detail": "Not found."
        },
        status=404)
    try:
        cloudscale = Cloudscale(api_token="token")
        cloudscale.server.get_by_uuid(uuid="unknown")
    except CloudscaleApiException as e:
        assert e.status_code == 404
        assert str(e) == "API Response Error (404): Not found."
        assert e.response == {'data': {'detail': 'Not found.'}, 'status_code': 404}

@responses.activate
def test_server_get_auth_not_provided():
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/servers/unknown',
        json={
            "detail": "Authentication credentials were not provided."
        },
        status=401)
    try:
        cloudscale = Cloudscale(api_token="token")
        cloudscale.server.get_by_uuid(uuid="unknown")
    except CloudscaleApiException as e:
        assert e.status_code == 401
        assert str(e) == "API Response Error (401): Authentication credentials were not provided."

@responses.activate
def test_server_create():
    name = "db-master"
    flavor = "flex-4"
    image = "debian9"

    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/servers',
        json=SERVER_RESP,
        status=204)

    cloudscale = Cloudscale(api_token="token")
    cloudscale.server.create(
        name=name,
        flavor=flavor,
        image=image,
    )

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server',
        '-a', 'token',
        'create',
        '--name',
        name,
        '--flavor',
        flavor,
        '--image',
        image
    ])
    assert result.exit_code == 0

@responses.activate
def test_server_update():
    uuid = "47cec963-fcd2-482f-bdb6-24461b2d47b1"
    name = "db-master"
    responses.add(
        responses.PATCH,
        CLOUDSCALE_API_ENDPOINT + '/servers/' + uuid,
        json=SERVER_RESP,
        status=204)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/servers/' + uuid,
        json=SERVER_RESP,
        status=200)

    cloudscale = Cloudscale(api_token="token")
    server = cloudscale.server.update(uuid=uuid, name=name)
    assert server['name'] == name
    assert server['uuid'] == uuid
    assert server['tags']['project'] == "gemini"

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server',
        '-a', 'token',
        'update',
        '--uuid',
        uuid,
        '--name',
        name,
    ])
    assert result.exit_code == 0

@responses.activate
def test_server_start():
    uuid = "47cec963-fcd2-482f-bdb6-24461b2d47b1"
    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/servers/' + uuid + '/start',
        status=204)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/servers/' + uuid,
        json=SERVER_RESP,
        status=200)

    cloudscale = Cloudscale(api_token="token")
    server = cloudscale.server.start(uuid=uuid)
    assert server is None

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server',
        '-a', 'token',
        'start',
        '--uuid',
        uuid,
    ])
    assert result.exit_code == 0

@responses.activate
def test_server_stop():
    uuid = "47cec963-fcd2-482f-bdb6-24461b2d47b1"
    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/servers/' + uuid + '/stop',
        status=204)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/servers/' + uuid,
        json=SERVER_RESP,
        status=200)

    cloudscale = Cloudscale(api_token="token")
    server = cloudscale.server.stop(uuid=uuid)
    assert server is None

    runner = CliRunner()
    result = runner.invoke(cli, [
        'server',
        '-a', 'token',
        'stop',
        '--uuid',
        uuid,
    ])
    assert result.exit_code == 0
