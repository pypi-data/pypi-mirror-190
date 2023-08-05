from datetime import datetime

from nazca4sdk.datahandling.kafka.kafka_sender import KafkaSender
from nazca4sdk.datahandling.knowledge.knowledge_data_type import KnowledgeDataType
from nazca4sdk.datahandling.open_data_client import OpenDataClient
from datetime import timezone


class KnowledgeStorage:

    def __init__(self, https=True):
        self.__openData = OpenDataClient(https)
        self.__kafkaSender = KafkaSender()

    def read_keys(self, name: str = None, ts_min: str = None, ts_max: str = None, size: int = 0):
        def validate(date):
            try:
                if date is None:
                    return True
                datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
                return True
            except:
                print("Incorrect datetime format, should be YYYY-MM-DDTHH:MM:SS")
                return False

        if not validate(ts_min):
            return None
        if not validate(ts_max):
            return None

        if ts_min is None:
            ts_min_str = None
        else:
            dt_ts_min = datetime.strptime(ts_min, '%Y-%m-%dT%H:%M:%S')
            ts_min_str = dt_ts_min.strftime("%Y%m%dT%H%M%S")

        if ts_max is None:
            ts_max_str = None
        else:
            dt_ts_max = datetime.strptime(ts_max, '%Y-%m-%dT%H:%M:%S')
            ts_max_str = dt_ts_max.strftime("%Y%m%dT%H%M%S")

        return self.__openData.read_knowledge_keys(name, ts_min_str, ts_max_str, size)

    def read_key_values(self, key: str):
        return self.__openData.read_knowledge_values(key)

    def write_key_values(self, key: str, section: str, value: str, datatype: KnowledgeDataType):
        if not KnowledgeDataType.has_value(datatype):
            print(f"KafkaDataType has no value  {datatype}")
            return None
        current_timestamp = datetime.now(timezone.utc).isoformat()
        data_dict = {"timestamp": current_timestamp,
                     "key": key,
                     "property": section,
                     "value": value,
                     "dataType": datatype.value}
        return self.__kafkaSender.send_message("dataflow.fct.knowledge", key, data_dict)

    def delete_keys(self, keys):
        return self.__openData.delete_knowledge_keys(keys)

    def delete_sections(self, sections, key):
        return self.__openData.delete_knowledge_sections(sections, key)
