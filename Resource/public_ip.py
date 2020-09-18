from record import Record


class PublicIpUsageRecord(Record):
    """
    Class to represent one public ip record.

    """
    all_records = []

    def __init__(self):
        Record.__init__(self)
        self._mandatory_fields = ["MeasurementTime", "SiteName", "CloudType", "LocalUser", "LocalGroup",
                                  "GlobalUserName", "FQAN", "IPVersion", "IPCount"]
        self._msg_fields = ["MeasurementTime", "SiteName", "CloudType", "LocalUser", "LocalGroup", "GlobalUserName",
                            "FQAN", "IPVersion", "IPCount", "CloudComputeService"]

        self._all_fields = self._msg_fields
        self._db_fields = self._msg_fields

        self._int_fields = ["IpCount", ]
        self._unix_timestamp_fields = ["MeasurementTime", ]
        PublicIpUsageRecord.all_records.append(self)

    def _check_fields(self):
        Record._check_fields(self)

    def output(self):
        return self.get_json()