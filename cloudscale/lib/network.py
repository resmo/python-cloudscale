from . import CloudscaleMutable

class Network(CloudscaleMutable):

    def __init__(self):
        super().__init__()
        self.resource = 'networks'
