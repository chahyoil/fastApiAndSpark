from fastapi import APIRouter, Query, Depends
from pyspark.sql import SparkSession
from sql.constructor_queries import GET_CONSTRUCTOR_STANDINGS, GET_CONSTRUCTOR_RESULTS, GET_CONSTRUCTOR_STANDINGS_COUNT
from utils.spark_utils import get_spark
from utils.json_utils import spark_to_json
from utils.error_handlers import handle_exception
from utils.pagination import paginate
from dto.constructor_dto import ConstructorStandingsResponse, ConstructorResultsResponse, ConstructorStanding, ConstructorResult

router = APIRouter()

@router.get("/standings", response_model=ConstructorStandingsResponse)
@paginate(GET_CONSTRUCTOR_STANDINGS_COUNT, GET_CONSTRUCTOR_STANDINGS, response_model=ConstructorStanding)
async def get_constructor_standings(
    year: int = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    spark: SparkSession = Depends(get_spark)
    ):
    """
    팀 순위를 조회하는 엔드포인트
    
    :param year: 조회할 연도 (선택적)
    :return: 지정된 연도의 팀 순위 데이터
    """
    return {}

@router.get("/{constructor_id}/results", response_model=ConstructorResultsResponse)
def get_constructor_results(constructor_id: int, year: int = Query(None), spark: SparkSession = Depends(get_spark)):
    """
    특정 팀의 결과를 조회하는 엔드포인트
    
    :param constructor_id: 조회할 팀의 ID
    :param year: 조회할 연도 (선택적)
    :return: 지정된 팀과 연도의 결과 데이터
    """
    try:
        # SQL 쿼리 렌더링
        query = GET_CONSTRUCTOR_RESULTS.render(constructor_id=constructor_id, year=year)
        
        # 쿼리 실행 및 결과 반환
        result = spark.sql(query)
        constructor_results = spark_to_json(result, ConstructorResult)
        return ConstructorResultsResponse(constructor_results=constructor_results)
    
    except Exception as e:
        raise handle_exception(e)
