from fastapi import APIRouter, Query, Depends
from sql.circuit_queries import GET_CIRCUIT_INFO, GET_CIRCUIT_RACES, GET_ALL_CIRCUITS, GET_CIRCUITS_COUNT
from utils.spark_utils import get_spark
from utils.json_utils import spark_to_json
from utils.error_handlers import handle_exception
from utils.pagination import paginate
from dto.circuit_dto import CircuitResponse, CircuitInfoResponse, CircuitInfo, CircuitRace, CircuitRaceResponse, Circuit
from pyspark.sql import SparkSession
router = APIRouter()

@router.get("/", response_model=CircuitResponse)
@paginate(GET_CIRCUITS_COUNT, GET_ALL_CIRCUITS, response_model=Circuit)
async def get_circuits(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    spark: SparkSession = Depends(get_spark)
):
    """
    모든 서킷 목록을 조회하는 엔드포인트
    """
    return {}

@router.get("/{circuit_id}", response_model=CircuitInfoResponse)
def get_circuit_info(circuit_id: int, spark: SparkSession = Depends(get_spark)):
    try:
        
        
        # Circuit Info 쿼리 실행 및 변환
        query = GET_CIRCUIT_INFO.render(circuit_id=circuit_id)
        result = spark.sql(query)
        circuit_info = spark_to_json(result, CircuitInfo)[0]

        # Circuit Races 쿼리 실행 및 변환
        query = GET_CIRCUIT_RACES.render(circuit_id=circuit_id)
        result = spark.sql(query)
        races = spark_to_json(result, CircuitRace)

        return CircuitInfoResponse(circuit_info=circuit_info, races=races)
    except Exception as e:
        raise handle_exception(e)

@router.get("/{circuit_id}/races", response_model=CircuitRaceResponse)
def get_circuit_races(circuit_id: int, spark: SparkSession = Depends(get_spark)):
    """
    특정 서킷에서 열린 레이스 정보를 가져오는 엔드포인트
    
    :param circuit_id: 서킷 ID
    :return: 해당 서킷의 레이스 정보를 포함하는 딕셔너리
    """
    try:
        # SQL 쿼리 렌더링
        query = GET_CIRCUIT_RACES.render(circuit_id=circuit_id)
        
        # 쿼리 실행 및 결과 변환
        result = spark.sql(query)
        circuit_races = spark_to_json(result, CircuitRace)
        return CircuitRaceResponse(circuit_races=circuit_races)
    except Exception as e:
        raise handle_exception(e)
