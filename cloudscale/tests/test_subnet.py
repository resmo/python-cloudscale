from cloudscale import Cloudscale, CloudscaleApiException, CloudscaleException, CLOUDSCALE_API_ENDPOINT
from cloudscale.cli import cli
import responses
import click
from click.testing import CliRunner

SUBNET_RESP = {
    "href": "https://api.cloudscale.ch/v1/subnets/33333333-1864-4608-853a-0771b6885a3a",
    "uuid": "33333333-1864-4608-853a-0771b6885a3a",
    "cidr": "192.0.2.123/24",
    "network": {
        "href": "https://api.cloudscale.ch/v1/networks/2db69ba3-1864-4608-853a-0771b6885a3a",
        "uuid": "2db69ba3-1864-4608-853a-0771b6885a3a",
        "name": "my-network-name",
    },
    "tags": {}
}

@responses.activate
def test_subnet_get_all():
    uuid = "33333333-1864-4608-853a-0771b6885a3a"
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/subnets',
        json=[SUBNET_RESP],
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/subnets',
        json=[SUBNET_RESP],
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/subnets',
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    subnets = cloudscale.subnet.get_all()
    assert subnets[0]['uuid'] == uuid

    runner = CliRunner()
    result = runner.invoke(cli, [
        'subnet',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'subnet',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code > 0

@responses.activate
def test_subnet_get_by_uuid():
    uuid = "33333333-1864-4608-853a-0771b6885a3a"
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/subnets/' + uuid,
        json=SUBNET_RESP,
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/subnets/' + uuid,
        json=SUBNET_RESP,
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/subnets/' + uuid,
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    subnet = cloudscale.subnet.get_by_uuid(uuid=uuid)
    assert subnet['uuid'] == uuid

    runner = CliRunner()
    result = runner.invoke(cli, [
        'subnet',
        '-a', 'token',
        'show',
        uuid,
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'subnet',
        '-a', 'token',
        'show',
        uuid,
    ])
    assert result.exit_code > 0

def test_subnet_missing_api_key():
    runner = CliRunner()
    result = runner.invoke(cli, [
        'subnet',
        'list',
    ])
    assert result.exit_code == 1
