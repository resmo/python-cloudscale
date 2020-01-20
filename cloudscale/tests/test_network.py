from cloudscale import Cloudscale, CloudscaleApiException, CloudscaleException, CLOUDSCALE_API_ENDPOINT
from cloudscale.cli import cli
import responses
import click
from click.testing import CliRunner

NETWORK_RESP = {
    "href": "https://api.cloudscale.ch/v1/networks/2db69ba3-1864-4608-853a-0771b6885a3a",
    "uuid": "2db69ba3-1864-4608-853a-0771b6885a3a",
    "name": "my-network-name",
    "created_at": "2019-05-29T13:18:42.511407Z",
    "zone": {
        "slug": "lpg1"
    },
    "mtu": 9000,
    "subnets": [
        {
        "href": "https://api.cloudscale.ch/v1/subnets/33333333-1864-4608-853a-0771b6885a3a",
        "uuid": "33333333-1864-4608-853a-0771b6885a3a",
        "cidr": "172.16.0.0/24"
        }
    ],
    "tags": {}
}

@responses.activate
def test_network_get_all():
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/networks',
        json=[NETWORK_RESP],
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/networks',
        json=[NETWORK_RESP],
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/networks',
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    networks = cloudscale.network.get_all()
    assert networks[0]['name'] == "my-network-name"
    assert networks[0]['uuid'] == "2db69ba3-1864-4608-853a-0771b6885a3a"

    runner = CliRunner()
    result = runner.invoke(cli, [
        'network',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'network',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code > 0

@responses.activate
def test_network_get_by_uuid():
    uuid = "2db69ba3-1864-4608-853a-0771b6885a3a"
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/networks/' + uuid,
        json=NETWORK_RESP,
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/networks/' + uuid,
        json=NETWORK_RESP,
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/networks/' + uuid,
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    network = cloudscale.network.get_by_uuid(uuid=uuid)
    assert network['name'] == "my-network-name"
    assert network['uuid'] == uuid

    runner = CliRunner()
    result = runner.invoke(cli, [
        'network',
        '-a', 'token',
        'show',
        uuid,
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'network',
        '-a', 'token',
        'show',
        uuid,
    ])
    assert result.exit_code > 0

@responses.activate
def test_network_delete():
    uuid = "2db69ba3-1864-4608-853a-0771b6885a3a"
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/networks/' + uuid,
        json=NETWORK_RESP,
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/networks/unknown',
        json=NETWORK_RESP,
        status=200)
    responses.add(
        responses.DELETE,
        CLOUDSCALE_API_ENDPOINT + '/networks/' + uuid,
        status=204)
    responses.add(
        responses.DELETE,
        CLOUDSCALE_API_ENDPOINT + '/networks/unknown',
        json={
            "detail": "Not found."
        },
        status=404)

    cloudscale = Cloudscale(api_token="token")
    network = cloudscale.network.delete(uuid=uuid)
    assert network is None

    try:
        cloudscale = Cloudscale(api_token="token")
        cloudscale.network.delete(uuid="unknown")
    except CloudscaleApiException as e:
        assert e.status_code == 404

    runner = CliRunner()
    result = runner.invoke(cli, [
        'network',
        '-a', 'token',
        'delete',
        uuid,
    ])
    assert result.exit_code == 1
    runner = CliRunner()
    result = runner.invoke(cli, [
        'network',
        '-a', 'token',
        'delete',
        uuid,
        '--force',
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'network',
        '-a', 'token',
        'delete',
        '--force',
        'unknown',
    ])
    assert result.exit_code > 0

@responses.activate
def test_network_create():
    name = "my-network-name"

    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/networks',
        json=NETWORK_RESP,
        status=201)
    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/networks',
        json=NETWORK_RESP,
        status=201)
    responses.add(
        responses.POST,
        CLOUDSCALE_API_ENDPOINT + '/networks',
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    cloudscale.network.create(
        name=name,
    )

    runner = CliRunner()
    result = runner.invoke(cli, [
        'network',
        '-a', 'token',
        'create',
        '--name',
        name,
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'network',
        '-a', 'token',
        'create',
        '--name',
        name,
    ])
    assert result.exit_code > 0


@responses.activate
def test_network_update():
    uuid = "2db69ba3-1864-4608-853a-0771b6885a3a"
    name = "my-network-name"
    responses.add(
        responses.PATCH,
        CLOUDSCALE_API_ENDPOINT + '/networks/' + uuid,
        json=NETWORK_RESP,
        status=204)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/networks/' + uuid,
        json=NETWORK_RESP,
        status=200)
    responses.add(
        responses.PATCH,
        CLOUDSCALE_API_ENDPOINT + '/networks/' + uuid,
        json=NETWORK_RESP,
        status=204)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/networks/' + uuid,
        json=NETWORK_RESP,
        status=200)
    responses.add(
        responses.PATCH,
        CLOUDSCALE_API_ENDPOINT + '/networks/' + uuid,
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    network = cloudscale.network.update(uuid=uuid, name=name)
    assert network['name'] == name
    assert network['uuid'] == uuid

    runner = CliRunner()
    result = runner.invoke(cli, [
        'network',
        '-a', 'token',
        'update',
        uuid,
        '--name',
        name,
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'network',
        '-a', 'token',
        'update',
        uuid,
        '--name',
        name,
    ])
    assert result.exit_code > 0

@responses.activate
def test_network_get_by_uuid_not_found():
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/networks/unknown',
        json={
            "detail": "Not found."
        },
        status=404)
    try:
        cloudscale = Cloudscale(api_token="token")
        cloudscale.network.get_by_uuid(uuid="unknown")
    except CloudscaleApiException as e:
        assert e.status_code == 404
        assert str(e) == "API Response Error (404): Not found."
        assert e.response == {'data': {'detail': 'Not found.'}, 'status_code': 404}

def test_network_missing_api_key():
    runner = CliRunner()
    result = runner.invoke(cli, [
        'network',
        'list',
    ])
    assert result.exit_code == 1
