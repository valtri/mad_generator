from records import CloudRecords, StorageRecords, IpRecords
from cloud import CloudRecord
from storage import StorageRecord
from public_ip import PublicIpUsageRecord

from example.storage_example import storage_json
from example.public_ip_example import ip_json
from example.cloud_example import cloud_json

cr = CloudRecords()
for i in range(0,10):
    c = CloudRecord()
    c.set_all(cloud_json)
    cr.add_record(c)
cr.generate()

cr = StorageRecords()
for i in range(0,10):
    c = StorageRecord()
    c.set_all(storage_json)
    cr.add_record(c)
cr.generate()

cr = IpRecords()
for i in range(0,10):
    c = PublicIpUsageRecord()
    c.set_all(ip_json)
    cr.add_record(c)
cr.generate()