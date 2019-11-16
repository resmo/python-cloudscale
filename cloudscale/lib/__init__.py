__metaclass__ = type

class CloudscaleBase:

    def __init__(self):
        self.verbose = False
        self.client = None
        self.resource = None

    def get_all(self, filter_tag=None):
        if filter_tag is not None:
            if '=' in filter_tag:
                tag_key, tag_value = filter_tag.split('=')
            else:
                tag_key = filter_tag
                tag_value = None

            if not tag_key.startswith('tag:'):
                tag_key = 'tag:%s' % tag_key

            payload = {
                tag_key: tag_value
            }
        else:
            payload = None

        return self.client.get_resources(self.resource, payload=payload)


class CloudscaleMutable(CloudscaleBase):

    def get_by_uuid(self, uuid):
        return self.client.get_resources(self.resource, resource_id=uuid)

    def delete(self, uuid):
        return self.client.delete_resource(self.resource, resource_id=uuid)

    def update(self, **kwargs):
        raise NotImplementedError
