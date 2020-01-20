import os
import configparser
from .client import RestAPI
from .lib.server import Server
from .lib.server_group import ServerGroup
from .lib.volume import Volume
from .lib.flavor import Flavor
from .lib.floating_ip import FloatingIp
from .lib.image import Image
from .lib.region import Region
from .lib.network import Network
from .lib.subnet import Subnet
from .lib.objects_user import ObjectsUser

from .error import CloudscaleException, CloudscaleApiException # noqa F401

from .version import __version__

APP_NAME = 'cloudscale-cli'
CLOUDSCALE_API_ENDPOINT = 'https://api.cloudscale.ch/v1'
CLOUDSCALE_CONFIG = 'cloudscale.ini'


class Cloudscale:

    def __init__(self, api_token=None, profile=None, verbose=False):

        if api_token and profile:
            raise CloudscaleException("API token and profile are mutually exclusive")

        # Read ini configs
        self.config = self._read_from_configfile(profile=profile)

        if api_token:
            self.api_token = api_token
        else:
            self.api_token = self.config.get('api_token')

        # Configre requests timeout
        self.timeout = self.config.get('timeout', 60)

        if not self.api_token:
            raise CloudscaleException("Missing API key: see -h for help")

        self.verbose = verbose
        self.service_classes = {
            'server': Server,
            'server_group': ServerGroup,
            'volume': Volume,
            'flavor': Flavor,
            'floating_ip': FloatingIp,
            'image': Image,
            'region': Region,
            'network': Network,
            'subnet': Subnet,
            'objects_user': ObjectsUser,
        }


    def _read_from_configfile(self, profile=None):

        config_file = os.getenv('CLOUDSCALE_CONFIG', CLOUDSCALE_CONFIG)

        paths = (
            os.path.join(os.path.expanduser('~'), '.{}'.format(config_file)),
            os.path.join(os.getcwd(), config_file),
        )

        conf = configparser.ConfigParser()
        conf.read(paths)

        if profile:
            if profile not in conf._sections:
                raise CloudscaleException("Profile '{}' not found in config files: ({})".format(profile, ', '. join(paths)))
        else:
            profile = os.getenv('CLOUDSCALE_PROFILE', 'default')

        if not conf._sections.get(profile):
            return dict()

        return dict(conf.items(profile))


    def __getattr__(self, name):
        try:
            client = RestAPI(
                api_token=self.api_token,
                endpoint=CLOUDSCALE_API_ENDPOINT,
                user_agent="python-cloudscale {}".format(__version__),
                timeout=self.timeout,
            )
            obj = self.service_classes[name]()
            obj._client = client
            obj.verbose = self.verbose
            return obj
        except KeyError as e:
            msg = "{} not implemented".format(e)
            raise NotImplementedError(msg)
