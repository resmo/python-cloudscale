__metaclass__ = type

class CloudscaleApiException(Exception):
    def __init__(self, *args, **kwargs):
        self.result = kwargs.pop('result')
        self.message = kwargs.pop('message')

class CloudscaleBase:

    def __init__(self):
        self.verbose = False
        self._client = None
        self.resource = None

    def _handle_exception(self, result):
        if result.get('status_code') not in (200, 201, 204):
            message = result.get('data', dict()).get('detail', 'Unknown error')
            raise CloudscaleApiException(message=message, result=result)
        return result

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

        result = self._client.get_resources(self.resource, payload=payload)
        return self._handle_exception(result)


class CloudscaleMutable(CloudscaleBase):

    def get_by_uuid(self, uuid):
        result = self._client.get_resources(self.resource, resource_id=uuid)
        return self._handle_exception(result)

    def delete(self, uuid):
        result = self._client.delete_resource(self.resource, resource_id=uuid)
        return self._handle_exception(result)

    def update(self, uuid, payload):
        result = self._client.post_patch_resource(self.resource, resource_id=uuid, payload=payload)
        return self._handle_exception(result)

    def create(self, payload):
        result = self._client.post_patch_resource(self.resource, payload=payload)
        return self._handle_exception(result)
