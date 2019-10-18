from .client import RestAPI
__metaclass__ = type

__version__ = '0.0.1'
APP_NAME = 'cloudscale-cli'
CLOUDSCALE_API_ENDPOINT = 'https://api.cloudscale.ch/v1'

class Cloudscale:

    def __init__(self, api_key):
        self.api_key = api_key
        self.service_classes = {
            'server': Server,
            'server_group': ServerGroup,
            'volume': Volume,
            'flavor': Flavor,
            'floating_ip': FloatingIp,
            'image': Image,
        }

    def __getattr__(self, name):
        try:
            return self.service_classes[name](self.api_key)
        except NameError as e:
            raise


class CloudscaleBase:

    def __init__(self, api_key, verbose):
        self.verbose = verbose
        self.client = RestAPI(
            api_key=api_key,
            endpoint=CLOUDSCALE_API_ENDPOINT
        )
        self.resource = None

    def get_all(self):
        return self.client.get_resources(self.resource)


class CloudscaleMutable(CloudscaleBase):

    def get_by_uuid(self, uuid):
        return self.client.get_resources(self.resource, resource_id=uuid)

    def delete(self, uuid):
        return self.client.delete_resource(self.resource, resource_id=uuid)


class ServerGroup(CloudscaleMutable):

    def __init__(self, api_key, verbose=False):
        super(ServerGroup, self).__init__(api_key, verbose)
        self.resource = 'server-groups'

    def create(self, name, group_type=None, tags=None):
        payload = {
            'name': name,
            'type': group_type,
            'tags': tags,
        }
        return self.client.post_patch_resource(self.resource, payload=payload)

    def update(self, uuid, name=None, tags=None):
        payload = {
            'name': name,
            'tags': tags,
        }
        return self.client.post_patch_resource(self.resource, resource_id=uuid, payload=payload)


class Server(CloudscaleMutable):

    def __init__(self, api_key, verbose=False):
        super(Server, self).__init__(api_key, verbose)
        self.resource = 'servers'

    def create(self, name, group_type=None, tags=None):
        payload = {
            'name': name,
            'tags': tags,
        }
        return self.client.post_patch_resource(self.resource, payload=payload)

    def update(self, uuid, name=None, tags=None):
        payload = {
            'name': name,
            'tags': tags,
        }
        return self.client.post_patch_resource(self.resource, resource_id=uuid, payload=payload)


class Volume(CloudscaleMutable):

    def __init__(self, api_key, verbose=False):
        super(Volume, self).__init__(api_key, verbose)
        self.resource = 'volumes'


class FloatingIp(CloudscaleMutable):

    def __init__(self, api_key, verbose=False):
        super(FloatingIp, self).__init__(api_key, verbose)
        self.resource = 'floating-ips'


class Flavor(CloudscaleBase):

    def __init__(self, api_key, verbose=False):
        super(Flavor, self).__init__(api_key, verbose)
        self.resource = 'flavors'


class Image(CloudscaleBase):

    def __init__(self, api_key, verbose=False):
        super(Image, self).__init__(api_key, verbose)
        self.resource = 'images'
