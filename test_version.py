from cloudscale.cli import cli
import click
from click.testing import CliRunner


def test_version():

    runner = CliRunner()
    result = runner.invoke(cli, [
        'version',
    ])
    assert result.exit_code == 0
