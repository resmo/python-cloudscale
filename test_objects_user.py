from cloudscale import Cloudscale, CloudscaleApiException, CloudscaleException, CLOUDSCALE_API_ENDPOINT
from cloudscale.cli import cli
import responses
import click
from click.testing import CliRunner

OBJECTS_USER_RESP = {
    "href": "https://api.cloudscale.ch/v1/objects-users/6fe39134bf4178747eebc429f82cfafdd08891d4279d0d899bc4012db1db6a15",
    "id": "6fe39134bf4178747eebc429f82cfafdd08891d4279d0d899bc4012db1db6a15",
    "display_name": "alan",
    "keys": [
        {
            "access_key": "0ZTAIBKSGYBRHQ09G11W",
            "secret_key": "bn2ufcwbIa0ARLc5CLRSlVaCfFxPHOpHmjKiH34T"
        }
    ],
    "tags": {}
}

@responses.activate
def test_objects_user_get_all():
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/objects-users',
        json=[OBJECTS_USER_RESP],
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/objects-users',
        json=[OBJECTS_USER_RESP],
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/objects-users',
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    objects_users = cloudscale.objects_user.get_all()
    assert objects_users[0]['display_name'] == "alan"
    assert objects_users[0]['id'] == "6fe39134bf4178747eebc429f82cfafdd08891d4279d0d899bc4012db1db6a15"

    runner = CliRunner()
    result = runner.invoke(cli, [
        'objects-user',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'objects-user',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code > 0

@responses.activate
def test_objects_user_get_by_uuid():
    uuid = "6fe39134bf4178747eebc429f82cfafdd08891d4279d0d899bc4012db1db6a15"
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/' + uuid,
        json=OBJECTS_USER_RESP,
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/' + uuid,
        json=OBJECTS_USER_RESP,
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/' + uuid,
        json={},
        status=500)
    cloudscale = Cloudscale(api_token="token")
    objects_user = cloudscale.objects_user.get_by_uuid(uuid=uuid)
    assert objects_user['display_name'] == "alan"
    assert objects_user['id'] == uuid

    runner = CliRunner()
    result = runner.invoke(cli, [
        'objects-user',
        '-a', 'token',
        'show',
        '--uuid',
        uuid,
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'objects-user',
        '-a', 'token',
        'show',
        '--uuid',
        uuid,
    ])
    assert result.exit_code > 0

@responses.activate
def test_objects_user_delete():
    uuid = "6fe39134bf4178747eebc429f82cfafdd08891d4279d0d899bc4012db1db6a15"

    responses.add(
        responses.DELETE,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/' + uuid,
        status=204)
    responses.add(
        responses.DELETE,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/' + uuid,
        status=204)
    responses.add(
        responses.DELETE,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/' + uuid,
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    objects_user = cloudscale.objects_user.delete(uuid=uuid)
    assert objects_user is None

    runner = CliRunner()
    result = runner.invoke(cli, [
        'objects-user',
        '-a', 'token',
        'delete',
        '--uuid',
        uuid,
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'objects-user',
        '-a', 'token',
        'delete',
        '--uuid',
        uuid,
    ])
    assert result.exit_code > 0

@responses.activate
def test_objects_user_get_by_uuid_not_found():
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/unknown',
        json={
            "detail": "Not found."
        },
        status=404)
    try:
        cloudscale = Cloudscale(api_token="token")
        cloudscale.objects_user.get_by_uuid(uuid="unknown")
    except CloudscaleApiException as e:
        assert e.status_code == 404
        assert str(e) == "API Response Error (404): Not found."
        assert e.response == {'data': {'detail': 'Not found.'}, 'status_code': 404}

@responses.activate
def test_objects_user_create():
    display_name = "alan"

    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/objects-users',
        json=OBJECTS_USER_RESP,
        status=201)
    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/objects-users',
        json=OBJECTS_USER_RESP,
        status=201)
    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/objects-users',
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    cloudscale.objects_user.create(
        display_name=display_name,
    )

    runner = CliRunner()
    result = runner.invoke(cli, [
        'objects-user',
        '-a', 'token',
        'create',
        '--display-name',
        display_name,
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'objects-user',
        '-a', 'token',
        'create',
        '--display-name',
        display_name,
    ])
    assert result.exit_code > 0

@responses.activate
def test_objects_user_update():
    uuid = "6fe39134bf4178747eebc429f82cfafdd08891d4279d0d899bc4012db1db6a15"
    display_name = "alan"
    responses.add(
        responses.PATCH,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/' + uuid,
        json=OBJECTS_USER_RESP,
        status=204)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/' + uuid,
        json=OBJECTS_USER_RESP,
        status=200)
    responses.add(
        responses.PATCH,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/' + uuid,
        json=OBJECTS_USER_RESP,
        status=204)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/' + uuid,
        json=OBJECTS_USER_RESP,
        status=200)
    responses.add(
        responses.PATCH,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/' + uuid,
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    objects_user = cloudscale.objects_user.update(uuid=uuid, display_name=display_name)
    assert objects_user['display_name'] == display_name
    assert objects_user['id'] == uuid

    runner = CliRunner()
    result = runner.invoke(cli, [
        'objects-user',
        '-a', 'token',
        'update',
        '--uuid',
        uuid,
        '--display-name',
        display_name,
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'objects-user',
        '-a', 'token',
        'update',
        '--uuid',
        uuid,
        '--display-name',
        display_name,
    ])
    assert result.exit_code > 0
