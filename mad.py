import argparse
import datetime
import cloud_data_types 
import xml_operations
import users
import logging
import random
#TODO: allow to set level to logs

parser = argparse.ArgumentParser(description='MAD Generator, simulator of Cloud life.')

parser.add_argument(
    '--output-type', 
    choices=['opennebulaxml', 'storagerecords'], 
    required=True,
    help='Output type of MAD Generator. opennebulaxml (OpenNebula XML) or storagerecords (Storage Records)'
)

parser.add_argument(
    '--count',
    type=int,
    required=True,
    help='The number of events to generate'
)

parser.add_argument(
    '--start-time',
    type=datetime.datetime.fromisoformat,
    default=datetime.datetime.today(),
    help='First TimeStamp of whole simulation - format YYYY-MM-DD'
)

parser.add_argument(
    '--max-objects',
    type=int,
    required=True,
    help='Max number of available existing objects'
)

#TODO: add average-filling (density)

parser.add_argument(
    '--cron-interval',
    # type=datetime.time.fromisoformat,
    # default=datetime.datetime.now(),
    #TODO: add time filter
    help='Intreval of "cron-triggered" events'
)
#TODO: know about interval and finish it

parser.add_argument(
    '--users-count',
    type=int,
    default=20,
    help='Users using simulated cloud'
)

parser.add_argument(
    '--groups-count',
    type=int,
    default=7,
    help='Groups in simulated cloud'
)

parser.add_argument(
    '--cloud-name',
    type=str,
    default='MADCLOUD',
    help='name of the cloud'
)
#TODO: use name

parser.add_argument(
    '--mode',
    choices=['vm', 'network', 'storage'],
    required=True,
    help='In which mode will MAD Generator run'
)

parser.add_argument(
    '-f',
    '--flood',
    action='store_true',
    default=False,
    help='Flood mode'
)

parser.add_argument(
    '-d',
    '--debug',
    action='store_false',
    default=True,
    help='Enable debug mode with logs'
)

CONF = parser.parse_args()

#---- Debug settings
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s:%(lineno)d - #%(process)d %(levelname)s: %(message)s')
if CONF.debug:
    logging.disable(logging.CRITICAL)
#----

logging.debug('Arguments parsed:')
logging.debug(CONF)

xml_operator = xml_operations.XmlOperator()
cloud_datastores = users.Datastores()

for x in range(CONF.users_count):

    # ---- modifying User
    user = cloud_data_types.User(CONF)

    xml_operator.output(user)
    # ----

if CONF.flood:

    for x in range(random.randint(1, CONF.max_objects)):

        # ---- modifying Vm
        vm = cloud_data_types.Vm(CONF)

        vm.uname = cloud_data_types.User.users_dict[vm.uid]['uname']
        vm.gid = cloud_data_types.User.users_dict[vm.uid]['gid']
        vm.gname = cloud_data_types.User.users_dict[vm.uid]['gname']

        xml_operator.output(vm)
        # ----

    for z in range(10):

        # ---- modifying Image
        image = cloud_data_types.Image(CONF)

        image.uname = cloud_data_types.User.users_dict[image.uid]['uname']
        image.gid = cloud_data_types.User.users_dict[image.uid]['gid']
        image.gname = cloud_data_types.User.users_dict[image.uid]['gname']

        datastore = cloud_datastores.getNewDatastore()

        image.datastore_id = datastore['datastore_id']
        image.datastore = datastore['datastore']

        xml_operator.output(image)
        # ----

    for z in range(10):

        # ---- modifying Host
        host = cloud_data_types.Host()

        xml_operator.output(host)
        # ----

    for z in range(10):

        # ---- modifying Cluster
        cluster = cloud_data_types.Cluster()

        xml_operator.output(cluster)
        # ----