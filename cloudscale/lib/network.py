from . import CloudscaleMutable

class Network(CloudscaleMutable):

    def __init__(self):
        super().__init__()
        self.resource = 'networks'

    def create(self, name, zone=None, mtu=None, auto_create_ipv4_subnet=None, tags=None):
        payload = {
            'name': name,
            'zone': zone,
            'mtu': mtu,
            'auto_create_ipv4_subnet': auto_create_ipv4_subnet,
            'tags': tags,
        }
        return super().create(payload=payload)

    def update(self, uuid, name=None, mtu=None, tags=None):
        payload = {
            'name': name,
            'mtu': mtu,
            'tags': tags,
        }
        return super().update(uuid=uuid, payload=payload)
