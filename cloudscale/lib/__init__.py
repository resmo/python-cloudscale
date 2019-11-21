from ..error import CloudscaleApiException

class CloudscaleBase:

    def __init__(self):
        self.verbose = False
        self._client = None
        self.resource = None

    def _process_response(self, response):
        status_code = response.get('status_code')
        data = response.get('data', dict())
        if status_code not in (200, 201, 204):
            raise CloudscaleApiException(
                "API Response Error ({0}): {1}".format(
                    status_code,
                    data.get('detail', data),
                ),
                response=response,
                status_code=status_code,
            )
        return data

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
        return self._process_response(result) or []


class CloudscaleBaseExt(CloudscaleBase):

    def get_by_uuid(self, uuid):
        response = self._client.get_resources(self.resource, resource_id=uuid)
        return self._process_response(response)


class CloudscaleMutable(CloudscaleBaseExt):

    def delete(self, uuid):
        response = self._client.delete_resource(self.resource, resource_id=uuid)
        return self._process_response(response)

    def update(self, uuid, payload):
        response = self._client.post_patch_resource(self.resource, resource_id=uuid, payload=payload)
        return self._process_response(response)

    def create(self, payload):
        response = self._client.post_patch_resource(self.resource, payload=payload)
        return self._process_response(response)
