from storage import StorageRecord
import datetime as dt
a = StorageRecord()

storage_json = dict()
storage_json["RecordId"] = "recordId"
storage_json["CreateTime"]= dt.datetime.now()
storage_json["StorageSystem"] = "ss"
storage_json["StorageShare"] = "50"
storage_json["StorageMedia"] = "video"
storage_json["FileCount"] = "1000"
storage_json["DirectoryPath"] = "/path/to/directory"
storage_json["LocalUser"] = "me"
storage_json["LocalGroup"] = "elixir"
storage_json["MeasureTime"] = dt.datetime.now()
storage_json["ValidDuration"] = dt.timedelta(0.051)
storage_json["ResourceCapacityUsed"] = 50
storage_json["LogicalCapacityUsed"] = 20
storage_json["Group"] = "grupa"
storage_json["Role"] = "role"
storage_json["StorageClass"] = "?????"
storage_json["UserIdentity"] = "meine identitat"
#a.set_all(storage_json)

