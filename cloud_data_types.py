import uuid
from shutil import copyfile
import random
import time
import string
import logging
import users

class Vm:
    
    def __init__(self, CONF):
        self.id = uuid.uuid4().int & (1<<32)-1
        self.uid = random.randint(1, CONF.users_count)
        self.stime = round(time.time())
        self.__set_etime()
        self.__set_ip()
        logging.debug('Vm object created:')
        logging.debug(self.__dict__)

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

class Image:
    
    def __init__(self, CONF):
        self.id = uuid.uuid4().int & (1<<32)-1
        self.uid = random.randint(1, CONF.users_count)
        self.regtime = round(time.time())
        self.size = random.randint(15, 150)
        self.cloudkeeper_appliance_mpuri = 'mpuri' + str(self.id)
        #TODO: finish mpuri after lenka answer
        logging.debug('Image object created:')
        logging.debug(self.__dict__)

class User:
    count = 0
    users_dict = {}

    def __init__(self, CONF):
        User.count = User.count + 1
        self.id = User.count
        self.uname = 'User' + str(self.id)
        self.gid = random.randint(1, CONF.groups_count)
        self.gname = 'Group' + str(self.gid)
        self.identity = users.generateRandomLowerString()
        User.users_dict[self.id] = self.__dict__
        logging.debug('User object created:')
        logging.debug(self.__dict__)
        # TODO: finish User class and work with it )

class Host:

    def __init__(self):
        self.id = uuid.uuid4().int & (1<<32)-1
        self.benchmark_value = users.generateRandomLowerString()
        logging.debug('Host object created:')
        logging.debug(self.__dict__)

class Cluster:

    def __init__(self):
        self.id = uuid.uuid4().int & (1<<32)-1
        self.benchmark_type = users.generateRandomLowerString()
        self.benchmark_value = users.generateRandomLowerString()
        logging.debug('Cluster object created:')
        logging.debug(self.__dict__)