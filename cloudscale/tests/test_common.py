import os
import click
import responses
from cloudscale import Cloudscale, CloudscaleApiException, CloudscaleException, CLOUDSCALE_API_ENDPOINT
from cloudscale.cli import cli
from click.testing import CliRunner
from configparser import ConfigParser
from ..util import tags_to_dict


class TestClass():

    CLOUDSCALE_CONFIG = os.getenv('CLOUDSCALE_CONFIG')

    def setup_class(self):
        config = ConfigParser()
        config.update({
            'test': {
                'api_token': 'test_token',
            },
            'default': {
                'api_token': 'default_token',
            },
        })

        # TODO: better solution?
        if self.CLOUDSCALE_CONFIG and self.CLOUDSCALE_CONFIG.startswith('/tmp/'):
            with open(self.CLOUDSCALE_CONFIG, 'w') as configfile:    # save
                config.write(configfile)

    def test_config_ini(self):
        if self.CLOUDSCALE_CONFIG:


            cloudscale = Cloudscale(profile="test")
            assert cloudscale.api_token == "test_token"

            cloudscale = Cloudscale()
            assert cloudscale.api_token == "default_token"

            try:
                cloudscale = Cloudscale(profile="does-not-exist")
            except CloudscaleException as e:
                assert str(e).startswith("Profile 'does-not-exist' not found in config files:")

    def teardown_class(self):
        if os.path.exists(self.CLOUDSCALE_CONFIG):
            os.remove(self.CLOUDSCALE_CONFIG)


def test_missing_api_key():
    try:
        cloudscale = Cloudscale(api_token=None)
    except CloudscaleException as e:
        assert str(e) == "Missing API key: see -h for help"

def test_mutually_exclusvie_api_key_and_profile():
    try:
        cloudscale = Cloudscale(api_token="token", profile="test")
    except CloudscaleException as e:
        assert str(e) == "API token and profile are mutually exclusive"

@responses.activate
def test_exception_returns():
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/unknown',
        json={
            "detail": "Not found."
        },
        status=404)
    responses.add(
        responses.GET,
        CLOUDSCALE_API_ENDPOINT + '/objects-users/unknown',
        json={},
        status=500)

    try:
        cloudscale = Cloudscale(api_token="token")
        cloudscale.objects_user.get_by_uuid(uuid="unknown")
    except CloudscaleApiException as e:
        assert e.status_code == 404
        assert str(e) == "API Response Error (404): Not found."
        assert e.response == {'data': {'detail': 'Not found.'}, 'status_code': 404}
    try:
        cloudscale = Cloudscale(api_token="token")
        cloudscale.objects_user.get_by_uuid(uuid="unknown")
    except CloudscaleApiException as e:
        assert e.status_code == 500
        assert e.response == {'data': {}, 'status_code': 500}
        assert str(e) == "API Response Error (500): {}"

def test_not_implemented():
    try:
        cloudscale = Cloudscale(api_token="token")
        cloudscale.foobar.get_by_uuid(uuid="unknown")
    except NotImplementedError as e:
        assert str(e) == "'foobar' not implemented"

def test_list_commands():
    runner = CliRunner()
    result = runner.invoke(cli, [
    ])
    assert result.exit_code == 0
