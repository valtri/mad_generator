import random
import string
import logging
import time

#TODO: rename file (consult with guru Taras)

class Users:

    def __init__(self):
        self.users_dict = {}
        logging.debug('Users object created')

    def addUser(self, uid):
        # username_length = random.randint(7, 12)
        # letters = string.ascii_letters

        # username = ''.join(random.choice(letters) for i in range(username_length)) + str(random.randint(10, 999))
        username = 'User' + str(uid)

        self.users_dict[uid] = username

        logging.debug('User ' + username + ' added to users_dict with id ' + str(uid))

class Groups:

    def __init__(self):
        self.groups_dict = {}
        logging.debug('Groups object created')

    def addGroup(self, gid):
        # groupname_length = random.randint(5, 10)
        # letters = string.ascii_lowercase

        # groupname = ''.join(random.choice(letters) for i in range(groupname_length)) + '-group'
        groupname = 'Group' + str(gid)

        self.groups_dict[gid] = groupname

        logging.debug('Group ' + groupname + ' added to groups_dict with id ' + str(gid))

class Datastores:

    def __init__(self):
        self.datastores_count = 0
        logging.debug('Datastores object created')

    def getNewDatastore(self):
        self.datastores_count = self.datastores_count + 1

        datastore_info = {
            'datastore_id': self.datastores_count,
            'datastore': 'datastore' + str(self.datastores_count)
        }

        return datastore_info

# class Regtimes:

#     def __init__(self, first_time = time.time()):
#         self.first_time = first_time
#         self.last_time = None

#     def getTime(self):
#         if self.last_time:
#             # return_time = self.last_time + random.randint
#             return 'last time exists'
#         else:
#             self.last_time = self.first_time
#             return self.first_time

def generateRandomLowerString():
    string_length = random.randint(10, 20)
    letters = string.ascii_lowercase

    return ''.join(random.choice(letters) for i in range(string_length))
#TODO: maybe move it or make it class