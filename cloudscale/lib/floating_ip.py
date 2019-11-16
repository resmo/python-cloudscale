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
        tags=None,
    ):
        payload = {
            'ip_version': ip_version,
            'prefix_length': prefix_length,
            'reverse_ptr': reverse_ptr,
            'server': server_uuid,
            'tags': tags,
        }
        return self.client.post_patch_resource(self.resource, payload=payload)
