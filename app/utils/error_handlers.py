import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

def handle_exception(e: Exception, error_message: str = "내부 서버 오류가 발생했습니다."):
    """
    예외를 처리하고 로깅하는 공통 함수
    
    :param e: 발생한 예외
    :param error_message: 클라이언트에게 반환할 오류 메시지
    :return: HTTPException
    """
    logger.error(f"오류 발생: {str(e)}")
    return HTTPException(status_code=500, detail=error_message)

def handle_not_found(item_name: str):
    """
    리소스를 찾을 수 없을 때 사용하는 함수
    
    :param item_name: 찾을 수 없는 항목의 이름
    :return: HTTPException
    """
    logger.error(f"{item_name}을(를) 찾을 수 없습니다.")
    return HTTPException(status_code=404, detail=f"{item_name}을(를) 찾을 수 없습니다.")