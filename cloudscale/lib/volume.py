from . import CloudscaleMutable

class Volume(CloudscaleMutable):

    def __init__(self):
        super(Volume, self).__init__()
        self.resource = 'volumes'

    def create(self, name, server_uuids, size_gb, volume_type=None, zone=None, tags=None):
        payload = {
            'name': name,
            'server_uuids': server_uuids,
            'size_gb': size_gb,
            'type': volume_type,
            'zone': zone,
            'tags': tags,
        }
        return super().create(payload=payload)

    def update(self, uuid, name=None, server_uuids=None, size_gb=None, tags=None):
        payload = {
            'name': name,
            'server_uuids': server_uuids or None,
            'size_gb': size_gb,
            'tags': tags,
        }
        return super().update(uuid=uuid, payload=payload)
