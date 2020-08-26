from random import choices
from time import time
from actions import *
import os
from datetime import datetime
from cloud import CloudRecord
from storage import StorageRecord
from public_ip import PublicIpUsageRecord
import logging

class User:
    count = 0

    def __init__(self):
        self.user_id = "" + str(User.count)
        self.group_id = ""
        self.global_name = "GLobalNaMe"
        self.site_name = "goat-vm-site-name"
        self.role = None
        self.cloud_compute_service = None
        self.cloud_type = "goat-vm-cloud-type"
        self.vms = []
        User.count += 1

    def generate_vms(self, vm_count):
        for i in range(vm_count):
            cr = CloudRecord()
            cr.set_all({
                "VMUUID": "user-" + self.user_id + "-machine-" + str(len(self.vms) + 1),
                "SiteName": self.site_name,
                "MachineName": "machine" + str(len(self.vms) + 1),
                "LocalUserId": self.user_id,
                "LocalGroupId": self.group_id,
                "GlobalUserName": self.global_name,
                "CloudComputeService": self.cloud_compute_service,
                "CloudType": self.cloud_type,
                "FQAN": "/Group"+ self.group_id +"/Role=NULL/Capability=NULL",
                "Disk": (2**30)*randint(50, 200),
                "Memory": (2**30)*randint(1, 16),
                "PublicIPCount": randint(0, 2),
                "IPv4Count": 0,
                "IPv6Count": 0,
                "SuspendDuration": 0,
                "CpuDuration": 0,
                "WallDuration": 0,
                "CpuCount": randint(1, 8),
                "StorageUsage": 0
                })
            self.vms.append(cr)

    @staticmethod
    def generate_users(user_count):
        users = []
        for i in range(user_count):
            users.append(User())
        return users


class Generator:
    def __init__(self, start_time, cron_interval, event_count, user_count, vm_count_min, vm_count_max, groups_count,
                 cloud_name, per_file: int, end_time=None):
        self.start_time = int(start_time)
        self.cron_interval = cron_interval
        self.event_count = event_count
        self.user_count = user_count
        self.vm_count_min = vm_count_min
        self.vm_count_max = vm_count_max
        self.groups_count = groups_count
        self.cloud_name = cloud_name
        self.per_file = per_file
        if end_time is None:
            end_time = time()
        self.end_time = int(end_time)

    def _generate_cron_intervals(self):
        return [self.start_time + i * self.cron_interval
                for i in range(1, int((self.end_time - self.start_time) / self.cron_interval))]

    def _generate_event_times(self):
        interval_length = int((self.end_time - self.start_time) / self.event_count)
        res = [self.start_time, ]
        for i in range(self.event_count):
            res.append(res[-1] + randint(int(round(.8 * interval_length)), int(round(1.2 * interval_length))))
        return res

    def _simulate_cloud_life(self, vm: CloudRecord, events, intervals):
        i, j = 0, 0
        # TODO pridat logy
        for i in range (len(events)-1):
            memory = vm.get_field("Memory")
            cpu = vm.get_field("CpuCount")
            status = vm.get_field("Status")
            ip = vm.get_field("PublicIPCount")
            disk = vm.get_field("StorageUsage")

            while j < len(intervals) and events[i+1] > intervals[j] > events[i]:

                cloud_record = CloudRecord()
                cloud_record.load_from_msg(vm.get_msg())

                j += 1

            event = choices([start_machine, finish_machine, suspend_machine, allocate_ip, free_ip, allocate_memory,
                             free_memory, allocate_cpu, free_cpu, allocate_storage, free_storage],
                            k=1,
                            weights=[19, 1, 10, 19, 19, 19, 19, 19, 19, 19, 19])[0]

            if memory == 0 and event == free_memory:
                event = allocate_memory
            if cpu == 0 and event == free_cpu:
                event = allocate_cpu

            if ip == 0 and event == free_ip:
                event = allocate_ip

            if disk == 0 and event == free_storage:
                event = allocate_storage
            if status is None and (event == finish_machine or event == suspend_machine):
                event = start_machine

            if status == "suspended" and event == suspend_machine:
                continue
            if status == "started" and event == start_machine:
                continue
            if status == "completed":
                continue

            vm = event(vm, events[i])

    def _simulate_storage_life(self, user: User, cron_intervals):
        storages = []
        from math import ceil
        for i in range(ceil(self.event_count/self.user_count)):
            start = randint(self.start_time, self.end_time)
            end = randint(start, self.end_time)
            storages.append((start, end))

        for st in storages:
            capacity = randint(2**20, 2**30)
            storage_json = {"RECORD_ID": user.user_id + str(st[0]),  # TODO random generate
                            "STORAGE_SYSTEM": "ss",  # TODO
                            "STORAGE_SHARE": "datastore" + str(randint(1, 20)),
                            "STORAGE_MEDIA": "disk",
                            "FILE_COUNT": str(randint(1, 100)),
                            "DIRECTORY_PATH": None,
                            "LOCAL_USER": user.user_id,
                            "LOCAL_GROUP": user.group_id,
                            "START_TIME": datetime.fromtimestamp(st[0]),  # TODO
                            "END_TIME": datetime.fromtimestamp(0),
                            "RESOURCE_CAPACITY_USED": capacity,
                            "LOGICAL_CAPACITY_USED": capacity,
                            "RESOURCE_CAPACITY_ALLOCATED": capacity,
                            "GROUP": "/Group" + user.group_id + "/Role=NULL/Capability=NULL ",
                            "STORAGE_CLASS": None,
                            "USER_IDENTITY": user.global_name,  # todo
                            "CREATE_TIME": datetime.fromtimestamp(st[0])}
            StorageRecord().set_all(storage_json)
            for interval in cron_intervals:
                if st[0] <= interval <= st[1]:
                    storage_json["RECORD_ID"] = user.user_id + str(interval)
                    storage_json["CREATE_TIME"] = datetime.fromtimestamp(interval)
                    StorageRecord().set_all(storage_json)
            storage_json["RECORD_ID"] = user.user_id + str(st[1])
            storage_json["CREATE_TIME"] = datetime.fromtimestamp(st[1])
            storage_json["END_TIME"] = datetime.fromtimestamp(st[1])
            StorageRecord().set_all(storage_json)

    def _simulate_ip_life(self, user, cron_intervals):
        for interval in cron_intervals:
            new_ip_record = PublicIpUsageRecord()
            new_ip_record.set_all(
                {"MeasurementTime": interval,
                 "SiteName": user.site_name,
                 "CloudComputeService": user.cloud_compute_service,
                 "CloudType": user.cloud_type,
                 "LocalUser": user.user_id,
                 "LocalGroup": user.group_id,
                 "GlobalUserName": user.global_name,
                 "FQAN": "/Group"+user.group_id+"/Role=NULL/Capability=NULL",
                 "IPVersion": choice(["4", "6"]),
                 "IPCount": randint(1, 10)
                 })

    def generate_cloud_records(self):
        cron_intervals = self._generate_cron_intervals()
        users = User.generate_users(self.user_count)
        x=0
        events_count = 0
        for user in users:
            user.group_id += str(randint(1, self.groups_count))
            user.cloud_compute_service = self.cloud_name
            user.generate_vms(randint(self.vm_count_min, self.vm_count_max))
            x+=len(user.vms)
            for vm in user.vms:
                events = self._generate_event_times()
                events_count+=len(events)
                self._simulate_cloud_life(vm, events, cron_intervals)
        self.to_file(CloudRecord, self.per_file)
        logging.debug("number of cloud records "+str( len(CloudRecord.all_records)))
        logging.debug("number of vms "+str(x))
        logging.debug("number of cron generation " +str( len(cron_intervals)))
        logging.debug("event count "+str( events_count))
    def generate_storage_records(self):  # TODO
        cron_intervals = self._generate_cron_intervals()
        users = User.generate_users(self.user_count)
        for user in users:
            user.group_id += str(randint(1, self.groups_count))
            user.cloud_compute_service = self.cloud_name
            self._simulate_storage_life(user, cron_intervals)
        self.to_file(StorageRecord, self.per_file)

    def generate_ip_records(self):  # TODO check
        cron_intervals = self._generate_cron_intervals()
        users = User.generate_users(self.user_count)
        for user in users:
            user.group_id += str(randint(1, self.groups_count))
            user.cloud_compute_service = self.cloud_name
            self._simulate_ip_life(user, cron_intervals)

        self.to_file(PublicIpUsageRecord, self.per_file)

    def to_file(self, record_class, per_file: int):
        count = 0
        id = 0
        if not os.path.exists(record_class.__name__+"/"):
            os.mkdir(record_class.__name__+"/")
        f = open(record_class.__name__+"/" + "{0:014b}".format(id), "w")
        if record_class == CloudRecord:
            f.write("APEL-cloud-message: v0.4\n")
        if record_class == PublicIpUsageRecord:
            f.write('{"Ips": [\n')
        if record_class == StorageRecord:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n\n<STORAGES>')
        for r in record_class.all_records:
            if count >= per_file:
                count = 0
                id += 1
                if record_class == PublicIpUsageRecord:
                    f.write("]}")
                if record_class == StorageRecord:
                    f.write("</STORAGES>")

                f = open(record_class.__name__ + "/" + "{0:014b}".format(id), "w")
                if record_class == CloudRecord:
                    f.write("APEL-cloud-message: v0.4\n")
                if record_class == PublicIpUsageRecord:
                    f.write('{"Ips": [\n')
                if record_class == StorageRecord:
                    f.write('<?xml version="1.0" encoding="UTF-8"?>\n\n<STORAGES>')
            count += 1
            if record_class == CloudRecord:
                f.write("\n")
            f.write(str(r.output()))
            if record_class == PublicIpUsageRecord:
                f.write(",\n")
            if record_class == CloudRecord:
                f.write("%%\n")
        if count != 0:
            if record_class == PublicIpUsageRecord:
                f.write("]}")
            if record_class == StorageRecord:
                f.write("</STORAGES>")