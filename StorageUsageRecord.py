import xml.etree.cElementTree as ET


class StorageUsageRecord:
    def __init__(self,
                 record_identity,
                 storage_system,
                 subject_identity,
                 measure_time,
                 valid_duration,
                 resource_capacity_used,
                 root=None,
                 **args):
        required = [record_identity, storage_system, subject_identity, measure_time, valid_duration, resource_capacity_used]
        if root is None:
            root = ET.Element("StorageUsageRecord")
        self.root = root

        for r in required:
            root.append(r.root)
        for att in args.values():
            root.append(att.root)

    def generate(self, filename):
        ET.ElementTree(self.root).write(filename)


class StorageUsageRecords:
    def __init__(self, records):
        self.root = ET.Element("StorageUsageRecords")
        for record in records:
            self.root.append(record.root)

    def generate(self, filename):
        ET.ElementTree(self.root).write(filename)


class RecordIdentity:
    count = 1

    def __init__(self, time):
        self.root = ET.Element("RecordIdentity",
                               createTime=time,
                               recordId=str(RecordIdentity.count))
        RecordIdentity.count += 1


class SubjectIdentity:
    def __init__(self, identities):
        self.root = ET.Element("SubjectIdentity")
        for identity in identities:
            self.root.append(identity.root)


class Identity:
    #vyriesit group attribute
    def __init__(self, identity_type, value, group_attribute_type = None):
        if identity_type not in ["UserIdentity", "Group", "GroupAttribute", "LocalGroup",  "LocalUser"]:
            raise ValueError("wrong identity type")
        if identity_type == "GroupAttribute":
            self.root = ET.Element(identity_type, AttributeType=group_attribute_type)
        else:
            self.root = ET.Element(identity_type)
        self.root.text = value


class DefaultAttribute:
    def __init__(self, attribute_type, value):
        if attribute_type not in ["StorageShare", "StorageMedia", "StorageClass", "FileCount",  "DirectoryPath",
                                  "LogicalCapacityUsed", "ResourceCapacityUsed", "ValidDuration", "MeasureTime",
                                  "StorageSystem"]:
            raise ValueError("wrong attribute type")
        self.root = ET.Element(attribute_type)
        self.root.text = value

#
# storage_record = StorageUsageRecord(record_identity=RecordIdentity("time1"),
#                                     storage_system= "host.example.org",
#                                     subject_identity=[Identity("UserIdentity", "Andrej"),
#                                                       Identity("Group", "dataproject"),
#                                                       Identity("GroupAttribute", "ukusers", "subgroup")],
#                                     measure_time= "2010-10-11T09:31:40Z",
#                                     valid_duration="PT3600S",
#                                     resource_capacity_used="13617",
#                                     storage_media= "disk",
#                                     file_count="4",
#                                     logical_capacity_used="12345")

storage_record = StorageUsageRecord(record_identity=RecordIdentity("time1"),
                                    storage_system=DefaultAttribute("StorageSystem", "host.example.org"),
                                    subject_identity=SubjectIdentity([Identity("UserIdentity", "Andrej"),
                                                                      Identity("Group", "dataproject"),
                                                                      Identity("GroupAttribute", "ukusers", "subgroup")]),
                                    measure_time=DefaultAttribute("MeasureTime", "2010-10-11T09:31:40Z"),
                                    valid_duration=DefaultAttribute("ValidDuration", "PT3600S"),
                                    resource_capacity_used=DefaultAttribute("ResourceCapacityUsed", "13617"),
                                    storage_media=DefaultAttribute("StorageMedia", "disk"),
                                    file_count=DefaultAttribute("FileCount", "4"),
                                    logical_capacity_used=DefaultAttribute("LogicalCapacityUsed", "12345"))
records = StorageUsageRecords([storage_record,])
records.generate("filename.xml")
