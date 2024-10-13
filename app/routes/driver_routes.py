from fastapi import APIRouter, Query, HTTPException
from dto.driver_dto import DriverResponse, DriverDetailsResponse, DriverStandingsResponse, Driver, DriverDetails, DriverStanding
from sql.driver_queries import GET_DRIVER_DETAILS, GET_DRIVER_STANDINGS, GET_DRIVERS_COUNT, GET_ALL_DRIVERS
from utils.spark_utils import get_spark_session
from utils.json_utils import spark_to_json
from utils.error_handlers import handle_exception
from utils.pagination import paginate

router = APIRouter()

@router.get("/", response_model=DriverResponse)
@paginate(GET_DRIVERS_COUNT, GET_ALL_DRIVERS, response_model=Driver)
async def get_drivers(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    드라이버 목록을 조회합니다.
    """
    return {}

@router.get("/{driver_id}", response_model=DriverDetailsResponse)
def get_driver_details(driver_id: int):
    """
    드라이버의 상세 정보를 조회합니다.

    Args:
        driver_id (int): 조회할 드라이버의 ID

    Returns:
        dict: 드라이버의 상세 정보를 포함하는 딕셔너리

    Raises:
        HTTPException: Spark 쿼리 실행 중 오류 발생 시
    """
    try:
        # Spark 세션 생성
        spark = get_spark_session()
        
        # SQL 쿼리 렌더링
        query = GET_DRIVER_DETAILS.render(driver_id=driver_id)
        
        # 쿼리 실행 및 결과 변환
        result = spark.sql(query)

        driver_details = spark_to_json(result, DriverDetails)[0]
        return DriverDetailsResponse(driver_details=driver_details)

    except Exception as e:
        raise handle_exception(e)

@router.get("/{driver_id}/standings", response_model=DriverStandingsResponse)
def get_driver_standings(driver_id: int, year: int = Query(None)):
    """
    드라이버의 순위 정보를 조회합니다.

    Args:
        driver_id (int): 조회할 드라이버의 ID
        year (int, optional): 조회할 연도. 기본값은 None으로, 전체 기간의 순위를 조회합니다.

    Returns:
        dict: 드라이버의 순위 정보를 포함하는 딕셔너리

    Raises:
        HTTPException: Spark 쿼리 실행 중 오류 발생 시
    """
    try:
        # Spark 세션 생성
        spark = get_spark_session()
        
        # SQL 쿼리 렌더링
        query = GET_DRIVER_STANDINGS.render(driver_id=driver_id, year=year)
        
        # 쿼리 실행 및 결과 변환
        result = spark.sql(query)
        driver_standings = spark_to_json(result, DriverStanding)

        return DriverStandingsResponse(driver_standings=driver_standings)
    except Exception as e:
        raise handle_exception(e)
