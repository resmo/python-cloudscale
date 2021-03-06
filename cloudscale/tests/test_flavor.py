from cloudscale import Cloudscale, CloudscaleApiException, CloudscaleException, CLOUDSCALE_API_ENDPOINT
from cloudscale.cli import cli
import responses
import click
from click.testing import CliRunner

FLAVOR_RESP = {
    "slug": "flex-2",
    "name": "Flex-2",
    "vcpu_count": 1,
    "memory_gb": 2,
    "zones": [
        {
            "slug": "rma1"
        },
        {
            "slug": "lpg1"
        }
    ]
}

@responses.activate
def test_flavor_get_all():
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/flavors',
        json=[FLAVOR_RESP],
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/flavors',
        json=[FLAVOR_RESP],
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/flavors',
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    flavors = cloudscale.flavor.get_all()
    assert flavors[0]['slug'] == "flex-2"
    assert flavors[0]['name'] == "Flex-2"

    runner = CliRunner()
    result = runner.invoke(cli, [
        'flavor',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'flavor',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code > 0

def test_flavor_missing_api_key():
    runner = CliRunner()
    result = runner.invoke(cli, [
        'flavor',
        'list',
    ])
    assert result.exit_code == 1
