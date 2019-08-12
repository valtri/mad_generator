import argparse
import datetime

parser = argparse.ArgumentParser(description='Process some integers.')

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
    help='Intreval of "cron-triggered" events'
)
#know about interval and finish it

parser.add_argument(
    '--cloud-name',
    type=str,
    default='MAD Cloud',
    help='name of the cloud'
)

parser.add_argument(
    '--mode',
    choices=['vm', 'network', 'storage'],
    required=True,
    help='In which mode will MAD Generator run'
)

CONF = parser.parse_args()

print(CONF.start_time)