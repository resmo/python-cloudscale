class CloudscaleException(Exception):
    pass

class CloudscaleApiException(Exception):

    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop('response')
        self.status_code = kwargs.pop('status_code')
