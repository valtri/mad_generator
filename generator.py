from datetime import datetime, timedelta
from random import randint
from cloud import CloudRecord
from storage import StorageRecord
from public_ip import PublicIpUsageRecord
from random import choice, choices
from time import time
from actions import *

class User:
    count = 0

    def __init__(self):
        self.user_id = "user-" + str(User.count)
        self.group_id = "group"
        self.global_name = "GLobalNaMe"
        self.site_name = "SiteName"
        self.role = None
        self.cloud_compute_service = None
        self.cloud_type = "OpenNebula??"
        self.vms = []
        User.count += 1

    def generate_vms(self, vm_count):
        for i in range(vm_count):
            cr = CloudRecord()
            cr.set_all({
                "VMUUID": self.user_id + "machine" +  str(len(self.vms) + 1),
                "SiteName": self.site_name,
                "MachineName": "machine" +  str(len(self.vms) + 1),
                "LocalUserId": self.user_id,
                "LocalGroupId": self.group_id,
                "GlobalUserName": self.global_name,
                "CloudComputeService": self.cloud_compute_service,
                "CloudType": self.cloud_type,
                "FQAN": "FQAN",
                "Disk": 0,
                "Memory": 0,
                "PublicIPCount": 0,
                "SuspendDuration": 0,
                "CpuDuration": 0,
                "WallDuration": 0,
                "CpuCount": 0,
                "StorageUsage": 0
                })
            self.vms.append(cr)


    @staticmethod
    def generate_users(user_count):
        users = []
        for i in range(user_count):
            users.append(User())
        return users


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
            "IPVersion": "dunno", # TODO co s tymto
            "IPCount": vm.get_field("PublicIPCount")
            }


class Generator:
    def __init__(self, start_time, cron_interval, event_count, user_count, vm_count_min, vm_count_max, groups_count, cloud_name, end_time = None):
        self.start_time = start_time
        self.cron_interval = cron_interval
        self.event_count = event_count
        self.user_count = user_count
        self.vm_count_min = vm_count_min
        self.vm_count_max = vm_count_max
        self.groups_count = groups_count
        self.cloud_name = cloud_name
        if end_time is None:
            end_time = time()
        self.end_time = end_time

    def _generate_cron_intervals(self):

        return [self.start_time + i * self.cron_interval
                for i in range(1, int((self.end_time - self.start_time) / self.cron_interval))]

    def _generate_event_times(self):
        interval_length = int((self.end_time - self.start_time) / self.event_count)
        res = [self.start_time, ]
        for i in range(self.event_count):
            res.append(res[-1] + randint(int(round(.8 * interval_length)), int(round(1.2 * interval_length))))
        return res

    def _simulate_life(self, vm: CloudRecord, events, intervals):
        i, j = 0, 0
        #TODO pridat logy
        for i in range (len(events)-1):
            memory = vm.get_field("Memory")
            cpu = vm.get_field("CpuCount")
            status = vm.get_field("Status")
            ip = vm.get_field("PublicIPCount")
            storage = vm.get_field("Disk")

            while j < len(intervals) and events[i+1] > intervals[j] > events[i]:
                new_storage_record = StorageRecord()
                new_storage_record.set_all(get_storage_json(vm, intervals[j]))

                new_ip_record = PublicIpUsageRecord()
                new_ip_record.set_all(get_ip_json(vm, intervals[j]))

                cloud_record = CloudRecord()
                cloud_record.load_from_msg(vm.get_msg())

                j += 1

            event = choices([start_machine, finish_machine, suspend_machine, allocate_ip, free_ip, allocate_memory,
                             free_memory, allocate_storage, free_storage, allocate_cpu, free_cpu],
                            k=1,
                            weights=[19, 1, 10, 19, 19, 19, 19, 19, 19,19, 19])[0]

            if memory == 0 and event == free_memory:
                event = allocate_memory
            if cpu == 0 and event == free_cpu:
                event = allocate_cpu
            if storage == 0 and event == free_storage:
                event = allocate_storage
            if ip == 0 and event == free_ip:
                event = allocate_ip

            if status is None and (event == finish_machine or event == suspend_machine):
                event = start_machine

            if status == "suspended" and event == suspend_machine:
                continue
            if status == "started" and event == start_machine:
                continue
            if status == "completed":
                continue

            event(vm, events[i])

    def generate_records(self):
        cron_intervals = self._generate_cron_intervals()
        users = User.generate_users(self.user_count)
        for user in users:
            user.group_id += str(randint(1, self.groups_count))
            user.cloud_compute_service = self.cloud_name
            user.generate_vms(randint(self.vm_count_min, self.vm_count_max))
            for vm in user.vms:
                events = self._generate_event_times()
                self._simulate_life(vm, events, cron_intervals)

    def to_file(self):
        pass