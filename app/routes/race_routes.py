from fastapi import APIRouter, HTTPException, Query
from dto.race_dto import RaceResponse, RaceDetailsResponse, RaceResultsResponse, FastestLapsResponse, Race, RaceDetails
from sql.race_queries import GET_RACE_RESULTS, GET_FASTEST_LAPS, GET_ALL_RACES, GET_RACE_DETAILS, GET_ALL_RACES_COUNT
from utils.spark_utils import get_spark_session
from utils.json_utils import spark_to_json
from utils.error_handlers import handle_exception
from utils.pagination import paginate
router = APIRouter()

@router.get("/", response_model=RaceResponse)
@paginate(GET_ALL_RACES_COUNT, GET_ALL_RACES, response_model=Race)
async def get_races(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    모든 레이스 목록을 조회하는 엔드포인트
    """
    return {}

@router.get("/{race_id}", response_model=RaceDetailsResponse)
async def get_race_details(race_id: int):
    """
    특정 레이스의 세부 정보를 조회하는 엔드포인트
    
    :param race_id: 조회할 레이스의 ID
    :return: 레이스 세부 정보
    """
    try:
        spark = get_spark_session()
        query = GET_RACE_DETAILS.render(race_id=race_id)
        result = spark.sql(query)
        if not spark_to_json(result):
            raise HTTPException(status_code=404, detail="Race not found")
        race_details = RaceDetails(**spark_to_json(result)[0])
        return RaceDetailsResponse(race_details=race_details)
    except Exception as e:
        raise handle_exception(e)

@router.get("/{race_id}/results", response_model=RaceResultsResponse)
async def get_race_results(race_id: int):
    """
    경주 결과를 조회하는 엔드포인트
    
    :param race_id: 조회할 경주의 ID
    :return: 경주 결과 데이터
    """
    try:
        spark = get_spark_session()
        query = GET_RACE_RESULTS.render(race_id=race_id)
        result = spark.sql(query)
        race_results = spark_to_json(result)
        return RaceResultsResponse(race_results=race_results)
    except Exception as e:
        raise handle_exception(e)

@router.get("/{race_id}/fastest-laps", response_model=FastestLapsResponse)
async def get_fastest_laps(race_id: int):
    """
    경주의 가장 빠른 랩 타임을 조회하는 엔드포인트
    
    :param race_id: 조회할 경주의 ID
    :return: 가장 빠른 랩 타임 데이터
    """
    try:
        spark = get_spark_session()
        query = GET_FASTEST_LAPS.render(race_id=race_id)
        result = spark.sql(query)
        fastest_laps = spark_to_json(result)
        return FastestLapsResponse(fastest_laps=fastest_laps)
    except Exception as e:
        raise handle_exception(e)
