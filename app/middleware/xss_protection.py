from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import html

class XSSProtectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 요청 파라미터에서 XSS 공격 가능성이 있는 문자열 이스케이프
        for param, value in request.query_params.items():
            request.query_params._dict[param] = html.escape(value)
        
        response = await call_next(request)
        return response