from cloud import CloudRecord
from random import randint, choice
from storage import StorageRecord
from public_ip import PublicIpUsageRecord
from _datetime import datetime


def get_storage_json(vm: CloudRecord, time: int):
    return {"RecordId": vm.get_field("LocalUserId") + str(time),  # TODO random generate
            "CreateTime": datetime.fromtimestamp(time),
            "StorageSystem": "ss",
            "StorageShare": "50",
            "StorageMedia": "disk",
            "FileCount": "1000",
            "DirectoryPath": None,
            "LocalUser": vm.get_field("LocalUserId"),
            "LocalGroup": vm.get_field("LocalGroupId"),
            "StartTime": datetime.fromtimestamp(time),  # TODO
            "EndTime": datetime.fromtimestamp(time),  # TODO ako tu ma byt start a end
            "ResourceCapacityUsed": vm.get_field("StorageUsage"),
            "LogicalCapacityUsed": vm.get_field("StorageUsage"),
            "ResourceCapacityAllocated": vm.get_field("StorageUsage"),
            "Group": None,  # not sure what
            "Role": None,  # neither here
            "StorageClass": None,
            "UserIdentity": vm.get_field("GlobalUserName")}


def get_ip_json(vm: CloudRecord, time: int):
    return {"MeasurementTime": time,
            "SiteName": vm.get_field("SiteName"),
            "CloudComputeService": vm.get_field("CloudComputeService"),
            "CloudType": vm.get_field("CloudType"),
            "LocalUser": vm.get_field("LocalUserId"),
            "LocalGroup": vm.get_field("LocalGroupId"),
            "GlobalUserName": vm.get_field("GlobalUserName"),
            "FQAN": vm.get_field("FQAN"),
            "IPVersion": "dunno", # TODO pouzijeme normalne version
            "IPCount": vm.get_field("PublicIPCount")
            }


def start_machine(vm: CloudRecord, event_time: int): #DONE
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    if vm.get_field("Status") == "suspended":
        vm.set_field("SuspendDuration",
                     vm.get_field("SuspendDuration") + (event_time - vm.get_field("SuspendTime")))
    vm.set_field("Status", "started")
    if vm.get_field("StartTime") is None:
        vm.set_field("StartTime", event_time)
    vm.set_field("CpuChange", event_time)


def finish_machine(vm: CloudRecord, event_time: int): # DONE
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    if vm.get_field("Status") == "started":
        vm.set_field("WallDuration",
                     vm.get_field("WallDuration") + (event_time - vm.get_field("CpuChange")))
        vm.set_field("CpuDuration",
                     vm.get_field("CpuDuration") +
                     vm.get_field("CpuCount")*(event_time - vm.get_field("CpuChange")))

    if vm.get_field("Status") == "suspended":
        vm.set_field("SuspendDuration",
                     vm.get_field("SuspendDuration") + (event_time - vm.get_field("SuspendTime")))

    vm.set_field("Status", "completed")
    vm.set_field("EndTime", event_time)


def suspend_machine(vm: CloudRecord, event_time: int):
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    vm.set_field("Status", "suspended")
    vm.set_field("SuspendTime", event_time)
    if vm.get_field("StartTime") is not None: #todo premysliet
        vm.set_field("WallDuration", (event_time - vm.get_field("CpuChange")))
        vm.set_field("CpuDuration", vm.get_field("CpuDuration") + vm.get_field("WallDuration")*vm.get_field("CpuCount"))


def allocate_ip(vm: CloudRecord, event_time: int):
    version = choice(["4", "6"])
    vm.set_field("IPv" + version + "Count", vm.get_field("IPv" + version + "Count") + randint(1,5))
    vm.set_field("PublicIpCount", vm.get_field("IPv4Count") + vm.get_field("IPv6Count"))


def free_ip(vm: CloudRecord, event_time: int):
    amount = randint(1, 5)
    version = choice(["4", "6"])
    if amount > vm.get_field("IPv" + version + "Count"):
        amount = vm.get_field("IPv" + version + "Count")
    vm.set_field("IPv" + version + "Count", vm.get_field("IPv" + version + "Count") - amount)
    vm.set_field("PublicIpCount", vm.get_field("IPv4Count") + vm.get_field("IPv6Count"))


def allocate_memory(vm:CloudRecord, event_time: int):
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    vm.set_field("Memory", vm.get_field("Memory") + (10**9)*randint(1,16))


def free_memory(vm:CloudRecord, event_time: int):
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    amount = (10**9)*randint(1,16)
    if amount > vm.get_field("Memory"):
        amount = vm.get_field("Memory")
    vm.set_field("Memory", vm.get_field("Memory") - amount)


# TODO zle
def allocate_storage(vm: CloudRecord, event_time: int):
    st = StorageRecord()
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    amount = (10**9)*randint(5, 1000)
    vm.set_field("StorageUsage", vm.get_field("StorageUsage") + amount)
    st.set_all(get_storage_json(vm, event_time))


# TODO zle, staci len vytvorit a zmazat ten storage
def free_storage(vm: CloudRecord, event_time: int):
    st = StorageRecord()
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())

    amount = (10 ** 9) * randint(5, 1000)
    if amount > vm.get_field("StorageUsage"):
        amount = vm.get_field("StorageUsage")
    vm.set_field("StorageUsage", vm.get_field("StorageUsage") - amount)
    st.set_all(get_storage_json(vm, event_time))


def allocate_cpu(vm: CloudRecord, event_time: int):
    amount = randint(1,32)
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    if vm.get_field("Status") == "started":
        vm.set_field("WallDuration", vm.get_field("WallDuration") + (event_time - vm.get_field("CpuChange"))) #nvm
        vm.set_field("CpuDuration", vm.get_field("CpuDuration")
                     + (event_time - vm.get_field("CpuChange"))*vm.get_field("CpuCount"))
    vm.set_field("CpuChange", event_time)
    vm.set_field("CpuCount", vm.get_field("CpuCount") + amount)


def free_cpu(vm: CloudRecord, event_time: int):
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    amount = randint(1, 32)
    if amount > vm.get_field("CpuCount"):
        amount = vm.get_field("CpuCount")
    if vm.get_field("Status") == "started":
        vm.set_field("WallDuration", vm.get_field("WallDuration") + (event_time - vm.get_field("StartTime")))
        vm.set_field("CpuDuration", vm.get_field("CpuDuration")
                     + (event_time - vm.get_field("CpuChange"))*vm.get_field("CpuCount"))
    vm.set_field("CpuChange", event_time)
    vm.set_field("CpuCount", vm.get_field("CpuCount") - amount)
