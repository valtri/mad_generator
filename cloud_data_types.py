import uuid
from shutil import copyfile
import random
import time
import string

class Vm:
    
    def __init__(self, CONF):
        self.id = uuid.uuid4().int & (1<<32)-1
        self.uid = random.randint(1, CONF.users_count)
        self.gid = random.randint(1, CONF.users_count/10)
        #TODO: randomize group max number, let user choose
        self.stime = round(time.time())
        self.__set_etime()
        self.__set_ip()

    def __set_etime(self):

        end_after = random.randint(0, 10800)

        if end_after == 0:
            self.etime = 0
        else:
            self.etime = self.stime + end_after

    def __set_ip(self):

        ip_type = random.randint(1, 2)

        if ip_type == 1:
            octets = []
            for x in range(4):
                octets.append(str(random.randint(0,255)))
            self.ip = '.'.join(octets)
    
        else:
            octets = []
            for x in range(8):
                octet = []
                for x in range(4):
                    octet.append(str(random.choice(string.hexdigits.lower())))
                octets.append(''.join(octet))
            self.ip = ':'.join(octets)