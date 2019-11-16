from . import CloudscaleMutable

class Network(CloudscaleMutable):

    def __init__(self):
        super(Network, self).__init__()
        self.resource = 'networks'
