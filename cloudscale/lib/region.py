from . import CloudscaleBase

class Region(CloudscaleBase):

    def __init__(self):
        super().__init__()
        self.resource = 'regions'
