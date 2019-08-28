import random
import string
import logging

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
        self.datastores_dict = {}
        logging.debug('Datastores object created')
    
    #TODO: finish datastores