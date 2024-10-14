from fastapi import APIRouter, Depends, HTTPException
from pyspark.sql import SparkSession
from utils.spark_utils import get_spark
from utils.json_utils import spark_to_json
from math import ceil
from utils.logging_utils import get_logger

router = APIRouter()

logger = get_logger(__name__)

@router.get("/all-tables")
def get_all_tables(spark: SparkSession = Depends(get_spark)):
    return {"tables": spark.catalog.listTables()}

@router.get("/table/{table_name}")
def get_table_columns(table_name: str, spark: SparkSession = Depends(get_spark)):
        #     "circuits","constructor_results", "constructor_standings","constructors","driver_standings",
        # "drivers","lap_times","pit_stops","qualifying", "races", "results","seasons","sprint_results","status"
    try:
        table = spark.table(table_name)
        columns = table.columns
        
        return {
            "table_name": table_name,
            "columns": columns
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"테이블을 찾을 수 없거나 오류가 발생했습니다: {str(e)}")

@router.get("/database-info")
def get_database_info(spark: SparkSession = Depends(get_spark)):
    try:
        
        current_database = spark.catalog.currentDatabase()
        databases = [db.name for db in spark.catalog.listDatabases()]
        logger.info(f"Current database: {current_database}")
        logger.info(f"Available databases: {databases}")
        return {
            "current_database": current_database,
            "databases": databases
        }
    except Exception as e:
        logger.error(f"Error fetching database info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"데이터베이스 정보를 가져오는 중 오류가 발생했습니다: {str(e)}")