# middleware/logging_middleware.py

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from utils.logging_utils import get_logger

logger = get_logger("api")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 요청 로깅
        logger.info(f"Request: {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        status_code = response.status_code
        
        # 응답 로깅
        logger.info(f"Response: {status_code} completed in {process_time:.4f}s")
        
        return response