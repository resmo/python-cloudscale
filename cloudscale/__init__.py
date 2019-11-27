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

__version__ = '0.6.0'

APP_NAME = 'cloudscale-cli'
CLOUDSCALE_API_ENDPOINT = 'https://api.cloudscale.ch/v1'


class Cloudscale:

    def __init__(self, api_token=None, profile=None, verbose=False):

        config = self._read_from_configfile(profile=profile)
        self.api_token = api_token or config.get('api_token')

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
        paths = (
            os.path.join(os.path.expanduser('~'), '.cloudscale.ini'),
            os.path.join(os.getcwd(), 'cloudscale.ini'),
        )

        conf = configparser.ConfigParser()
        conf.read(paths)

        if profile:
            if profile not in conf._sections:
                raise CloudscaleException("Profile not found in config files: {}, ({})".format(profile, ', '. join(paths)))
        else:
            profile = os.getenv('CLOUDSCALE_PROFILE', 'default')

        if not conf._sections.get(profile):
            return dict()

        return dict(conf.items(profile))


    def __getattr__(self, name):
        try:
            client = RestAPI(
                api_token=self.api_token,
                endpoint=CLOUDSCALE_API_ENDPOINT
            )
            obj = self.service_classes[name]()
            obj._client = client
            obj.verbose = self.verbose
            return obj
        except NameError as e:
            raise CloudscaleException(e)
