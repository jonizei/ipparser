
# filter type
ANY, LAST = range(2)

class IPFilter:

    def __init__(self, type):
        self.type = type

    def filter(self, ip):
        pass

    def get_type(self):
        return self.type