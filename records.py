from record import Record


class Records:
    def __init__(self):
        self.records = []
        self.name = ""

    def add_record(self, record: Record):
        self.records.append(record)

    def generate(self):
        name = "generated_"+ self.name + "_records"
        with open(name, "w") as output:
            for record in self.records:
                output.write(record.get_msg())
                output.write("%%\n")
        output.close()


class CloudRecords(Records):
    def __init__(self):
        Records.__init__(self)
        self.name = "cloud"


class IpRecords(Records):
    def __init__(self):
        Records.__init__(self)
        self.name = "ip"


class StorageRecords(Records):
    def __init__(self):
        Records.__init__(self)
        self.name = "storage"

    def generate(self):
        name = "generated_" + self.name + "_records"
        with open(name, "w") as output:
            output.write("<sr:StorageUsageRecords>")
            for record in self.records:
                output.write(record.get_ur())
            output.write("</sr:StorageUsageRecords>")
        output.close()
