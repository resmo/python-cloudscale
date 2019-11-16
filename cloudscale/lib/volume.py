from . import CloudscaleMutable

class Volume(CloudscaleMutable):

    def __init__(self):
        super(Volume, self).__init__()
        self.resource = 'volumes'
