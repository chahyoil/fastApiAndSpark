from fastapi import APIRouter, Query
from sql.f1_queries import GET_ALL_DRIVERS, GET_DRIVERS_COUNT, GET_DRIVER_BY_ID, GET_RACE_RESULTS, SPARK_EXAMPLE_QUERY
from utils.spark_utils import get_spark_session
from utils.json_utils import spark_to_json
from math import ceil

router = APIRouter()

@router.get("/drivers")
def get_drivers(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page")
):
    spark = get_spark_session()
    
    # Calculate the offset
    offset = (page - 1) * page_size
    
    # Get total count of drivers
    count_query = GET_DRIVERS_COUNT.render()
    total_count = spark.sql(count_query).first()['count']
    
    # Calculate total pages
    total_pages = ceil(total_count / page_size)
    
    # Render the query with pagination
    query = GET_ALL_DRIVERS.render(page_size=page_size, offset=offset)
    result = spark.sql(query)
    
    drivers = spark_to_json(result)
    
    return {
        "drivers": drivers,
        "page": page,
        "page_size": page_size,
        "total_items": total_count,
        "total_pages": total_pages
    }

@router.get("/drivers/{driver_id}")
def get_driver(driver_id: int):
    spark = get_spark_session()
    query = GET_DRIVER_BY_ID.render(driver_id=driver_id)
    result = spark.sql(query)
    driver_data = spark_to_json(result)
    return {"driver": driver_data[0] if driver_data else None}

@router.get("/race-results/{year}")
def get_race_results(year: int):
    spark = get_spark_session()
    query = GET_RACE_RESULTS.render(year=year)
    result = spark.sql(query)
    return {"race_results": spark_to_json(result)}

@router.get("/spark-example")
def spark_example():
    spark = get_spark_session()
    query = SPARK_EXAMPLE_QUERY.render(limit=10)
    result = spark.sql(query)
    return {"result": spark_to_json(result)}