from . import CloudscaleBase

class Flavor(CloudscaleBase):

    def __init__(self):
        super(Flavor, self).__init__()
        self.resource = 'flavors'
