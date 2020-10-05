# MAD Generator

A standalone program that simulates cloud life and generates accounting records based on received arguments . The program is used to generate consistent data for functional and scaling tests.

## Arguments

Run `python mad.py --help` to see arguments  

```
--output-type {opennebulaxml,records}
--count COUNT                           number of events per object machine/storage/ip 

optional:
--start-time START_TIME                 first timestamp of simulation, format: YYYY-MM-DD
--max-objects MAX_OBJECTS               
--average-occupancy AVERAGE_OCCUPANCY   average_occupance*max_objects/100 is mean number of generated machines  
--records-per-file RECORDS_PER_FILE     records stored in one file
--cron-interval CRON_INTERVAL           number interval between 2 cron record generations
--users-count USERS_COUNT               number of different users
--groups-count GROUPS_COUNT             number of different groups 
--cloud-name CLOUD_NAME                 cloud name to be used in records
--mode {vm,network,storage}             records type

-f, --flood                             flood mode - all mode options are chosen
-d, --debug                             debug                                              
```
## Example

```
python3 mad.py --output-type=opennebulaxml --count=5 --max-objects=10 --mode=vm -f

```
## Results
 
OpenNebula records:

`python3 mad.py --output-type=opennebulaxml`
[output example](https://github.com/goat-project/xmlrpc-server/tree/master/example_inputs)

Virtual machine records:

`python3 mad.py --output-type=records --mode=vm` 
[output example](https://github.com/goat-project/exporter/blob/master/parse/test-data/vm/0000_correctAPEL_10)

Storage records:

`python3 mad.py --output-type=records --mode=storage`
[output example](https://github.com/goat-project/exporter/blob/master/parse/test-data/st/0000_correctXML_10)

Public IP records:

`python3 mad.py --output-type=records --mode=network`
[output example](https://github.com/goat-project/exporter/blob/master/parse/test-data/ip/0000_correctJSON_20)

# Contributing
1.  Fork [MAD generator](https://github.com/CESNET/mad_generator/)
2.  Create your feature branch (git checkout -b my-new-feature)
3.  Commit your changes (git commit -am 'Add some feature')
4.  Push to the branch (git push origin my-new-feature)
5.  Create a new Pull Request
