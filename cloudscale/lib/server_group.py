from . import CloudscaleMutable

class ServerGroup(CloudscaleMutable):

    def __init__(self):
        super(ServerGroup, self).__init__()
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
        print(payload)
        return self.client.post_patch_resource(self.resource, resource_id=uuid, payload=payload)
