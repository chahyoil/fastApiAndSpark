from pydantic import BaseModel
from typing import Type, List
from pyspark.sql import Row
import json
from utils.logging_utils import get_logger

logger = get_logger(__name__)

def spark_to_json(spark_result, model: Type[BaseModel] = None):
    if isinstance(spark_result, list):
        result_list = spark_result
    else:
        result_list = spark_result.collect()
    
    dict_list = [row.asDict() if isinstance(row, Row) else row for row in result_list]
    
    def json_serializable(obj):
        if isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        return str(obj)
    
    json_data = json.loads(json.dumps(dict_list, default=json_serializable))
    logger.info(f"json_data: {json_data}")
    
    if model:
        return [model(**item) for item in json_data]
    return json_data