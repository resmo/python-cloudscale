from . import CloudscaleBase

class Image(CloudscaleBase):

    def __init__(self):
        super(Image, self).__init__()
        self.resource = 'images'
