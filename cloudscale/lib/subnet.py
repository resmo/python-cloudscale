from . import CloudscaleBaseExt

class Subnet(CloudscaleBaseExt):

    def __init__(self):
        super().__init__()
        self.resource = 'subnets'
