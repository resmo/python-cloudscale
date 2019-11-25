from cloudscale import Cloudscale, CloudscaleApiException, CloudscaleException, CLOUDSCALE_API_ENDPOINT
from cloudscale.cli import cli
import responses
import click
from click.testing import CliRunner

REGION_RESP = {
    "slug": "rma",
    "zones": [
        {
            "slug": "rma1"
        }
    ]
}


@responses.activate
def test_region_get_all():
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/regions',
        json=[REGION_RESP],
        status=200)

    cloudscale = Cloudscale(api_token="token")
    regions = cloudscale.region.get_all()
    assert regions[0]['slug'] == "rma"

    runner = CliRunner()
    result = runner.invoke(cli, [
        'region',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code == 0