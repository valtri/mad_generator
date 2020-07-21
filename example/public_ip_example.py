import time
from public_ip import  PublicIpUsageRecord

ip = PublicIpUsageRecord()
ip_json = {
    "SiteName": "CESNET-MCC",
    "LocalUser": "05228772e737467bbd5f5138d362d6a2",
    "FQAN": "vo.geoss.eu",
    "CloudType": "caso/1.3.3 (OpenStack)",
    "GlobalUserName": "529a87e5ce04cd5ddd7161734d02df0e2199a11452430803e714cb1309cc3907@egi.eu",
    "CloudComputeService": "CESNET-MCC",
    "MeasurementTime": time.time(),
    "LocalGroup": "local group",
    "IPVersion": "version4",
    "IPCount": 5}

#ip.set_all(ip_json)
#print(ip.get_msg())
