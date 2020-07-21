from cloud import CloudRecord

cloud = CloudRecord()
cloud_json = {"Memory": 8192,
        "Status": "started",
        "SiteName": "CESNET-MCC",
        "MachineName": "k8s-nodes-2",
        "WallDuration": 14018392,
        "CpuDuration": 56073568,
        "LocalUserId": "05228772e737467bbd5f5138d362d6a2",
        "FQAN": "vo.geoss.eu",
        "LocalGroupId": "24869cfe0e094f59a3110429e068eef2",
        "Disk": "3",
        "CpuCount": 4,
        "StartTime": 1561978603,
        "VMUUID": "13fed839-6381-4f6d-95dd-c40a825da36c",
        "CloudType": "caso/1.3.3 (OpenStack)",
        "GlobalUserName": "529a87e5ce04cd5ddd7161734d02df0e2199a11452430803e714cb1309cc3907@egi.eu",
        "CloudComputeService": "CESNET-MCC"}
#cloud.set_all(cloud_json)
#print(cloud.get_msg())