import argparse
import datetime
import cloud_data_types 
import xml_operations
import users
import logging
#TODO: make logs
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
    default=100,
    help='Users using simulated cloud'
)

#TODO: know about interval and finish it

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
    '--flood-mode',
    type=bool,
    default=True,
    help='Flood mode for generating with max speed'
)
#TODO: use/work with flood mode
#TODO: in flood generate start/reg times

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

# print(CONF.start_time)
#TODO: remove print time and work with it

xml_operator = xml_operations.XmlOperator()
cloud_users = users.Users()
cloud_groups = users.Groups()


for x in range(10):

    #---- modifying Vm
    vm = cloud_data_types.Vm(CONF)

    if vm.uid not in cloud_users.users_dict:
        cloud_users.addUser(vm.uid)

    if vm.gid not in cloud_groups.groups_dict:
        cloud_groups.addGroup(vm.gid)

    vm.uname = cloud_users.users_dict[vm.uid]
    vm.gname = cloud_groups.groups_dict[vm.gid]

    output_vm_kwargs_dict = {
        'id': vm.id,
        'uid': vm.uid,
        'uname': vm.uname,
        'gid': vm.gid,
        'gname': vm.gname,
        'stime': vm.stime,
        'etime': vm.etime,
        'ip': vm.ip
    }

    xml_operator.output('vm', **output_vm_kwargs_dict)
    #----

for z in range(10):

    # ---- modifying Image
    image = cloud_data_types.Image(CONF)

    if image.uid not in cloud_users.users_dict:
        cloud_users.addUser(image.uid)

    if image.gid not in cloud_groups.groups_dict:
        cloud_groups.addGroup(image.gid)

    image.uname = cloud_users.users_dict[image.uid]
    image.gname = cloud_groups.groups_dict[image.gid]

    output_image_kwargs_dict = {
        'id': image.id,
        'uid': image.uid,
        'uname': image.uname,
        'gid': image.gid,
        'gname': image.gname,
        'regtime': image.regtime
        #TODO: add datastore and finish
    }

    xml_operator.output('image' , **output_image_kwargs_dict)
    # ----