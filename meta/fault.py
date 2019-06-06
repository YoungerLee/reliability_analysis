class Fault(object):
    def __init__(self, id=0, pattern='', position='', reason='', root='', status=0, record_time=''):
        self.id = id
        self.pattern = pattern
        self.position = position
        self.reason = reason
        self.root = root
        self.status = status
        self.record_time = record_time

    def __hash__(self):
        return super(Fault, self).__hash__()
    def __lt__(self, other):
        return bool(self.id)
    def __eq__(self, other):
        return bool(self.id==other.id)
