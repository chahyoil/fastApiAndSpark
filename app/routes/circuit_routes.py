from fastapi import APIRouter, HTTPException, Query
from sql.circuit_queries import GET_CIRCUIT_INFO, GET_CIRCUIT_RACES, GET_ALL_CIRCUITS, GET_CIRCUITS_COUNT
from utils.spark_utils import get_spark_session
from utils.json_utils import spark_to_json
from utils.error_handlers import handle_exception
from utils.pagination import paginate
from dto.circuit_dto import CircuitResponse, CircuitInfoResponse, CircuitInfo, CircuitRace, CircuitRaceResponse, Circuit

router = APIRouter()

@router.get("/", response_model=CircuitResponse)
@paginate(GET_CIRCUITS_COUNT, GET_ALL_CIRCUITS, response_model=Circuit)
async def get_circuits(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    모든 서킷 목록을 조회하는 엔드포인트
    """
    return {}

@router.get("/{circuit_id}", response_model=CircuitInfoResponse)
def get_circuit_info(circuit_id: int):
    try:
        spark = get_spark_session()
        query = GET_CIRCUIT_INFO.render(circuit_id=circuit_id)
        result = spark.sql(query)
        circuit_info = CircuitInfo(**spark_to_json(result)[0])

        query = GET_CIRCUIT_RACES.render(circuit_id=circuit_id)
        result = spark.sql(query)
        races = [CircuitRace(**race) for race in spark_to_json(result)]

        return CircuitInfoResponse(circuit_info=circuit_info, races=races)
    except Exception as e:
        raise handle_exception(e)

@router.get("/{circuit_id}/races", response_model=CircuitRaceResponse)
def get_circuit_races(circuit_id: int):
    """
    특정 서킷에서 열린 레이스 정보를 가져오는 엔드포인트
    
    :param circuit_id: 서킷 ID
    :return: 해당 서킷의 레이스 정보를 포함하는 딕셔너리
    """
    try:
        # Spark 세션 가져오기
        spark = get_spark_session()
        
        # SQL 쿼리 렌더링
        query = GET_CIRCUIT_RACES.render(circuit_id=circuit_id)
        
        # 쿼리 실행 및 결과 변환
        result = spark.sql(query)
        circuit_races = spark_to_json(result)
        return CircuitRaceResponse(circuit_races=circuit_races)
    except Exception as e:
        raise handle_exception(e)
