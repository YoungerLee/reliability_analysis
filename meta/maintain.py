class Maintain(object):
    def __init__(self, id=0, maintain_date='1970-1-1', person='', maintain_time=0):
        self.id = id
        self.maintain_date = maintain_date
        self.person = person
        self.maintain_time = maintain_time

    def __hash__(self):
        return super(Maintain, self).__hash__()
    def __lt__(self, other):
        return bool(self.id)
    def __eq__(self, other):
        return bool(self.id==other.id)
