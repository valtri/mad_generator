import random
import logging
import time

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

class Regtimes:

    def __init__(self, first_time = time.time()):
        self.first_time = first_time
        self.last_time = None

    def getTime(self):
        if self.last_time:
            return_time = self.last_time + random.randint(1, random.randint(50, 150))
            self.last_time = return_time
            return return_time
        else:
            return_time = round(self.first_time)
            self.last_time = return_time
            return return_time