from fastapi import APIRouter, Query, HTTPException
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
