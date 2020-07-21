from record import Record, InvalidRecordException
from datetime import datetime
from datetime import timedelta


class PublicIpUsageRecord(Record):
    def __init__(self):
        Record.__init__(self)
        self._mandatory_fields = ["MeasurementTime", "SiteName", "CloudType","LocalUser","LocalGroup","GlobalUserName",
                                  "FQAN", "IPVersion", "IPCount"]
        self._msg_fields = ["MeasurementTime", "SiteName", "CloudType","LocalUser","LocalGroup","GlobalUserName",
                            "FQAN", "IPVersion", "IPCount","CloudComputeService"]
        # ip type vs ip version?

        self._all_fields = self._msg_fields
        self._db_fields = self._msg_fields

        self._int_fields = ["IpCount",]
        self._unix_timestamp_fields = ["MeasurementTime",]

    def _check_fields(self):
        Record._check_fields(self)
        self._check_timestamp()

    def _check_timestamp(self):
        try:
            timestamp = int(self._record_content["MeasurementTime"])
            if timestamp == 0:
                raise InvalidRecordException("Epoch time  mustn't be 0.")
            now = datetime.now()
            # add two days to prevent timezone problems
            tomorrow = now + timedelta(2)
            if datetime.fromtimestamp(timestamp) > tomorrow:
                raise InvalidRecordException("Epoch time " + str(timestamp) + " is in the future.")
        except ValueError:
            raise InvalidRecordException("Cannot parse an integer from timestamp.")
