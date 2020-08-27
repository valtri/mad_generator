import argparse
import datetime
import cloud_data_types
import xml_operations
import data_structures
import logging
import random
from math import floor, ceil
from generator import Generator

parser = argparse.ArgumentParser(description="MAD Generator, simulator of Cloud life.")

parser.add_argument(
    "--output-type",
    choices=["opennebulaxml", "records"],
    required=True,
    help="Output type of MAD Generator. opennebulaxml (OpenNebula XML) or records",
)

parser.add_argument(
    "--count",
    type=int,
    required=True,
    help="The number of events to generate"
)

parser.add_argument(
    "--start-time",
    type=datetime.datetime.fromisoformat,
    default=datetime.datetime.today() - datetime.timedelta(days=100),
    help="First TimeStamp of whole simulation - format YYYY-MM-DD",
)

parser.add_argument(
    "--max-objects",
    type=int,
    required=True,
    help="Max number of available existing objects",
)


parser.add_argument(
    "--average-occupancy",
    type=int,
    default=50,
    help="The percentage number of objects out of the maximum, which should exist on average",
)

parser.add_argument(
    "--records-per-file",
    type=int,
    default=500,
    help="Number of records to be stored per file. Default=500",
)

parser.add_argument(
    '--cron-interval',
    type=int,
    default=60*60*24,
    help='Intreval of "cron-triggered" events'
)

parser.add_argument(
    "--users-count", type=int, default=20, help="Users using simulated cloud"
)

parser.add_argument(
    "--groups-count", type=int, default=7, help="Groups in simulated cloud"
)

parser.add_argument(
    "--cloud-name", type=str, default="MADCLOUD", help="name of the cloud"
) # SiteName/CloudType/CloudComputeService


parser.add_argument(
    "--mode",
    choices=["vm", "network", "storage"],
    required=True,
    help="In which mode will MAD Generator run",
)

parser.add_argument(
    "-f", "--flood", action="store_true", default=False, help="Flood mode"
)

parser.add_argument(
    "-d",
    "--debug",
    action="store_false",
    default=True,
    help="Enable debug mode with logs",
)

CONF = parser.parse_args()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s:%(lineno)d - #%(process)d %(levelname)s: %(message)s",
)
if CONF.debug:
    logging.disable(logging.CRITICAL)

logging.debug("Arguments parsed:")
logging.debug(CONF)


if CONF.output_type == "opennebulaxml":
    xml_operator = xml_operations.XmlOperator()
    cloud_datastores = data_structures.Datastores()

    for x in range(CONF.users_count):

        user = cloud_data_types.User(CONF)
        print(user.uname)
        xml_operator.output(user)

    # flood means generating all types of outputs i.e. image, cluster, host, vm
    if CONF.flood:

        for x in range(random.randint(1, CONF.max_objects)):

            vm = cloud_data_types.Vm(CONF)

            vm.uname = cloud_data_types.User.users_dict[vm.uid]["uname"]
            vm.gid = cloud_data_types.User.users_dict[vm.uid]["gid"]
            vm.gname = cloud_data_types.User.users_dict[vm.uid]["gname"]

            xml_operator.output(vm)

        for z in range(10):

            image = cloud_data_types.Image(CONF)

            image.uname = cloud_data_types.User.users_dict[image.uid]["uname"]
            image.gid = cloud_data_types.User.users_dict[image.uid]["gid"]
            image.gname = cloud_data_types.User.users_dict[image.uid]["gname"]

            datastore = cloud_datastores.getNewDatastore()

            image.datastore_id = datastore["datastore_id"]
            image.datastore = datastore["datastore"]

            xml_operator.output(image)

        for z in range(10):

            host = cloud_data_types.Host()

            xml_operator.output(host)

        for z in range(10):

            cluster = cloud_data_types.Cluster()

            xml_operator.output(cluster)
else:
    gen = Generator(datetime.datetime.timestamp(CONF.start_time),
                    CONF.cron_interval,
                    CONF.count,
                    CONF.users_count,
                    int(floor((0.8 * CONF.average_occupancy / 100) * CONF.max_objects / CONF.users_count)),
                    int(ceil((1.2 * CONF.average_occupancy / 100) * CONF.max_objects / CONF.users_count)),
                    CONF.groups_count,
                    CONF.cloud_name,
                    CONF.records_per_file)

    if CONF.flood:
        logging.debug("FLOOD in record mode")
        gen.generate_cloud_records()
        gen.generate_ip_records()
        gen.generate_storage_records()
    else:
        if CONF.mode == "vm":
            logging.debug("Generating VM records")
            gen.generate_cloud_records()
        if CONF.mode == "storage":
            logging.debug("Generating Storage records")
            gen.generate_storage_records()
        if CONF.mode == "network":
            logging.debug("Generating Network records")
            gen.generate_ip_records()

