from fastapi import APIRouter, Query, HTTPException
from sql.f1_queries import GET_ALL_DRIVERS, GET_DRIVERS_COUNT, GET_DRIVER_BY_ID, GET_RACE_RESULTS, SPARK_EXAMPLE_QUERY
from utils.spark_utils import get_spark_session
from utils.json_utils import spark_to_json
from math import ceil

router = APIRouter()

@router.get("/all-tables")
def get_all_tables():
    spark = get_spark_session()
    return {"tables": spark.catalog.listTables()}

@router.get("/table/{table_name}")
def get_table_columns(table_name: str):
    try:
        spark = get_spark_session()
        table = spark.table(table_name)
        columns = table.columns
        
        return {
            "table_name": table_name,
            "columns": columns
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"테이블을 찾을 수 없거나 오류가 발생했습니다: {str(e)}")

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
