from cloudscale import Cloudscale, CloudscaleApiException, CloudscaleException, CLOUDSCALE_API_ENDPOINT
from cloudscale.cli import cli
import responses
import click
from click.testing import CliRunner

IMAGE_RESP = {
    "slug": "arch-18.06",
    "name": "Arch 18.06",
    "operating_system": "Arch",
    "default_username": "arch",
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
def test_image_get_all():
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/images',
        json=[IMAGE_RESP],
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/images',
        json=[IMAGE_RESP],
        status=200)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/images',
        json={},
        status=500)

    cloudscale = Cloudscale(api_token="token")
    images = cloudscale.image.get_all()
    assert images[0]['slug'] == "arch-18.06"
    assert images[0]['name'] == "Arch 18.06"

    runner = CliRunner()
    result = runner.invoke(cli, [
        'image',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code == 0
    result = runner.invoke(cli, [
        'image',
        '-a',
        'token',
        'list',
    ])
    assert result.exit_code > 0

def test_image_missing_api_key():
    runner = CliRunner()
    result = runner.invoke(cli, [
        'image',
        'list',
    ])
    assert result.exit_code == 1
