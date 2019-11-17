from . import CloudscaleMutable

class Server(CloudscaleMutable):

    def __init__(self):
        super(Server, self).__init__()
        self.resource = 'servers'

    def create(
        self,
        name,
        flavor,
        image,
        zone=None,
        volume_size=None,
        volumes=None,
        interfaces=None,
        ssh_keys=None,
        password=None,
        use_public_network=None,
        use_private_network=None,
        use_ipv6=None,
        server_groups=None,
        user_data=None,
        tags=None,
    ):
        payload = {
            'name': name,
            'flavor': flavor,
            'image': image,
            'zone': zone,
            'volumes': volumes,
            'interfaces': interfaces,
            'ssh_keys': ssh_keys,
            'password': password,
            'use_public_network': use_public_network,
            'use_private_network': use_private_network,
            'use_ipv6': use_ipv6,
            'server_groups': server_groups,
            'user_data': user_data,
            'tags': tags,
        }
        return self.client.post_patch_resource(self.resource, payload=payload)

    def update(
        self,
        uuid,
        name=None,
        flavor=None,
        tags=None,
    ):
        payload = {
            'name': name,
            'flavor': flavor,
            'tags': tags,
        }
        return self.client.post_patch_resource(self.resource, resource_id=uuid, payload=payload)