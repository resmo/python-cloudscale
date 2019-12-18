from . import CloudscaleMutable

class FloatingIp(CloudscaleMutable):

    def __init__(self):
        super(FloatingIp, self).__init__()
        self.resource = 'floating-ips'

    def create(
        self,
        ip_version,
        prefix_length=None,
        reverse_ptr=None,
        server_uuid=None,
        scope=None,
        region=None,
        tags=None,
    ):
        payload = {
            'ip_version': ip_version,
            'prefix_length': prefix_length,
            'reverse_ptr': reverse_ptr,
            'server': server_uuid,
            'type': scope,
            'region': region,
            'tags': tags,
        }
        return super().create(payload=payload)

    def update(self, uuid, reverse_ptr=None, server_uuid=None, tags=None):
        payload = {
            'reverse_ptr': reverse_ptr,
            'server': server_uuid,
            'tags': tags,
        }
        return super().update(uuid=uuid, payload=payload)
