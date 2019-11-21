from . import CloudscaleMutable

class ObjectsUser(CloudscaleMutable):

    def __init__(self):
        super().__init__()
        self.resource = 'objects-users'

    def create(self, display_name, tags=None):
        payload = {
            'display_name': display_name,
            'tags': tags,
        }
        return super().create(payload=payload)

    def update(self, uuid, display_name=None, tags=None):
        payload = {
            'display_name': display_name,
            'tags': tags,
        }
        return super().update(uuid=uuid, payload=payload)
