from cloud import CloudRecord
from random import randint, choice


def start_machine(vm: CloudRecord, event_time: int) -> CloudRecord:
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    if new_record.get_field("Status") == "suspended":
        new_record.set_field("SuspendDuration",
                             new_record.get_field("SuspendDuration") + (event_time - new_record.get_field("SuspendTime")))
    new_record.set_field("Status", "started")
    if new_record.get_field("StartTime") is None:
        new_record.set_field("StartTime", event_time)
    new_record.set_field("CpuChange", event_time)
    return new_record


def finish_machine(vm: CloudRecord, event_time: int) -> CloudRecord:
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    if new_record.get_field("Status") == "started":
        new_record.set_field("WallDuration",
                             new_record.get_field("WallDuration") + (event_time - new_record.get_field("CpuChange")))
        new_record.set_field("CpuDuration",
                             new_record.get_field("CpuDuration") +
                             new_record.get_field("CpuCount")*(event_time - new_record.get_field("CpuChange")))

    if new_record.get_field("Status") == "suspended":
        new_record.set_field("SuspendDuration",
                             new_record.get_field("SuspendDuration") + (event_time - new_record.get_field("SuspendTime")))

    new_record.set_field("Status", "completed")
    new_record.set_field("EndTime", event_time)
    return new_record


def suspend_machine(vm: CloudRecord, event_time: int) -> CloudRecord:
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    new_record.set_field("Status", "suspended")
    new_record.set_field("SuspendTime", event_time)
    if new_record.get_field("StartTime") is not None:
        new_record.set_field("WallDuration", (event_time - new_record.get_field("CpuChange")))
        new_record.set_field("CpuDuration",
                             new_record.get_field("CpuDuration") +
                             new_record.get_field("WallDuration")*new_record.get_field("CpuCount"))
    return new_record


def allocate_ip(vm: CloudRecord, event_time: int) -> CloudRecord:
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    version = choice(["4", "6"])
    new_record.set_field("IPv" + version + "Count", new_record.get_field("IPv" + version + "Count") + randint(1,5))
    new_record.set_field("PublicIPCount", new_record.get_field("IPv4Count") + new_record.get_field("IPv6Count"))
    return new_record


def free_ip(vm: CloudRecord, event_time: int) -> CloudRecord:
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    amount = randint(1, 5)
    version = choice(["4", "6"])
    if amount > new_record.get_field("IPv" + version + "Count"):
        amount = new_record.get_field("IPv" + version + "Count")
    new_record.set_field("IPv" + version + "Count", new_record.get_field("IPv" + version + "Count") - amount)
    new_record.set_field("PublicIPCount", new_record.get_field("IPv4Count") + new_record.get_field("IPv6Count"))
    return new_record


def allocate_memory(vm: CloudRecord, event_time: int):
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    new_record.set_field("Memory", new_record.get_field("Memory") + (10**9)*randint(1,16))
    return new_record


def free_memory(vm: CloudRecord, event_time: int) -> CloudRecord:
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    amount = (10**9)*randint(1,16)
    if amount > new_record.get_field("Memory"):
        amount = new_record.get_field("Memory")
    new_record.set_field("Memory", new_record.get_field("Memory") - amount)
    return new_record


def allocate_storage(vm: CloudRecord, event_time: int) -> CloudRecord:
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    amount = (10**9)*randint(5, 1000)
    new_record.set_field("StorageUsage", new_record.get_field("StorageUsage") + amount)
    return new_record


def free_storage(vm: CloudRecord, event_time: int) -> CloudRecord:
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())

    amount = (10 ** 9) * randint(5, 1000)
    if amount > new_record.get_field("StorageUsage"):
        amount = new_record.get_field("StorageUsage")
    new_record.set_field("StorageUsage", int(new_record.get_field("StorageUsage")) - amount)
    return new_record


def allocate_cpu(vm: CloudRecord, event_time: int) -> CloudRecord:
    amount = randint(1, 32)
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    if new_record.get_field("Status") == "started":
        new_record.set_field("WallDuration", new_record.get_field("WallDuration") + (event_time - new_record.get_field("CpuChange")))
        new_record.set_field("CpuDuration", new_record.get_field("CpuDuration")
                             + (event_time - new_record.get_field("CpuChange"))*new_record.get_field("CpuCount"))
    new_record.set_field("CpuChange", event_time)
    new_record.set_field("CpuCount", new_record.get_field("CpuCount") + amount)
    return new_record


def free_cpu(vm: CloudRecord, event_time: int) -> CloudRecord:
    new_record = CloudRecord()
    new_record.load_from_msg(vm.get_msg())
    amount = randint(1, 32)
    if amount > new_record.get_field("CpuCount"):
        amount = new_record.get_field("CpuCount")
    if new_record.get_field("Status") == "started":
        new_record.set_field("WallDuration", new_record.get_field("WallDuration") +
                             (event_time - new_record.get_field("StartTime")))
        new_record.set_field("CpuDuration", new_record.get_field("CpuDuration")
                             + (event_time - new_record.get_field("CpuChange"))*new_record.get_field("CpuCount"))
    new_record.set_field("CpuChange", event_time)
    new_record.set_field("CpuCount", vm.get_field("CpuCount") - amount)
    return new_record
