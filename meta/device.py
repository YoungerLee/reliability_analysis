class Device(object):
    def __init__(self, id=0, name='', num=''):
        self.id = id
        self.name = name
        self.num = num
    def __hash__(self):
        return super(Device, self).__hash__()

    def __lt__(self, other):
        return bool(self.id)
    def __eq__(self, other):
        return bool(self.id==other.id)
