from . import CloudscaleMutable

class ServerGroup(CloudscaleMutable):

    def __init__(self):
        super().__init__()
        self.resource = 'server-groups'

    def create(self, name, group_type=None, tags=None):
        payload = {
            'name': name,
            'type': group_type,
            'tags': tags,
        }
        return super().create(payload=payload)

    def update(self, uuid, name=None, tags=None):
        payload = {
            'name': name,
            'tags': tags,
        }
        return super().update(uuid=uuid, payload=payload)
