from fastapi import APIRouter, Depends, HTTPException
from pyspark.sql import SparkSession
from utils.spark_utils import get_spark
from utils.json_utils import spark_to_json
from math import ceil
from utils.logging_utils import get_logger
import time
from utils.spark_utils import get_spark_and_session_id
import asyncio
import random
import string
from pyspark.sql.functions import col, length, sum, udf
from pyspark.sql.types import StringType

router = APIRouter()

logger = get_logger(__name__)

@router.get("/test_spark_session_sync")
def test_spark_session_sync(spark_and_session: tuple = Depends(get_spark_and_session_id)):
    try:
        spark, session_id = spark_and_session

        logger.info(f"Processing synchronous request with session ID: {session_id}")

        # 랜덤 문자열 생성 함수
        def random_string(length):
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        # UDF로 등록
        random_string_udf = udf(random_string, StringType())

        # 데이터프레임 생성 및 랜덤 문자열 컬럼 추가
        df = spark.range(1000000)  # 행 수를 조절할 수 있습니다
        for i in range(5):  # 5개의 랜덤 문자열 컬럼 생성
            df = df.withColumn(f"random_col_{i}", random_string_udf(col("id") % 20 + 5))  # 5~24 길이의 랜덤 문자열

        # 각 컬럼의 문자열 길이 합계 계산
        result = df.select(*[sum(length(col(f"random_col_{i}"))).alias(f"sum_{i}") for i in range(5)]).collect()[0]

        # 결과를 딕셔너리로 변환
        result_dict = {f"sum_{i}": int(result[f"sum_{i}"]) for i in range(5)}
        result_dict["session_id"] = session_id

        return result_dict
    except Exception as e:
        logger.error(f"Error in test_spark_session_sync: {str(e)}")
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")
