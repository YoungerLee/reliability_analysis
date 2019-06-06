class Record(object):
    def __init__(self, id=0, run_time=0.0, env_temp=0.0, kni_temp=0.0, rpa=0.0, test_date='1970-01-01', axis='X'):
        self.id = id
        self.run_time = run_time
        self.env_temp = env_temp
        self.kni_temp = kni_temp
        self.rpa = rpa
        self.test_date = test_date
        self.axis = axis
    def __hash__(self):
        return super(Record, self).__hash__()
    def __lt__(self, other):
        return bool(self.id)
    def __eq__(self, other):
        return bool(self.id==other.id)
