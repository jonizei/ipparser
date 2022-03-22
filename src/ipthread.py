import threading
from tmphandler import *

class IPThread(threading.Thread):

    def __init__(self, threadId, name, tmp_from, tmp_to, filter):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.tmp_from = tmp_from
        self.tmp_to = tmp_to
        self.filter = filter

    def run(self):
        write_tmp_file(self.tmp_from, self.tmp_to, self.filter)
        print('runnung')