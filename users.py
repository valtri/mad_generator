import random
import string

#TODO: rename file (consult with guru Taras)

class Users:

    def __init__(self):
        self.users_dict = {}

    def addUser(self, uid):
        username_length = random.randint(7, 12)
        letters = string.ascii_letters

        username = ''.join(random.choice(letters) for i in range(username_length)) + str(random.randint(10, 999))

        self.users_dict[uid] = username

class Groups:

    def __init__(self):
        self.groups_dict = {}

    def addGroup(self, gid):
        groupname_length = random.randint(5, 10)
        letters = string.ascii_lowercase

        groupname = ''.join(random.choice(letters) for i in range(groupname_length)) + '-group'

        self.groups_dict[gid] = groupname