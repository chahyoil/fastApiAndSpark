from typing import Type
from pydantic import BaseModel
from fastapi import Query
from functools import wraps
from utils.spark_utils import get_spark_session
from utils.json_utils import spark_to_json
from math import ceil
from utils.logging_utils import get_logger

logger = get_logger(__name__)

def paginate(count_query_template, data_query_template, response_model: Type[BaseModel] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(
            page: int = Query(1, ge=1, description="Page number"),
            page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
            *args, **kwargs
        ):
            spark = get_spark_session()
            
            offset = (page - 1) * page_size
            
            count_query = count_query_template.render(**kwargs)
            total_count = spark.sql(count_query).first()['count']
            
            total_pages = ceil(total_count / page_size)
            
            query_params = {**kwargs, 'page_size': page_size, 'offset': offset}
            query = data_query_template.render(**query_params)
            result = spark.sql(query)
            
            if response_model:
                data = spark_to_json(result, model=response_model)
            else:
                data = spark_to_json(result)
            
            logger.info(f"data: {data}")
            
            response_data = {
                "data": data,
                "page": page,
                "page_size": page_size,
                "total_items": total_count,
                "total_pages": total_pages
            }
            
            return response_data
        return wrapper
    return decorator