from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from utils.auth import get_current_user, verify_admin

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 인증이 필요한 경로 패턴 정의
        protected_paths = ["/api/admin", "/api/protected"]
        
        if any(request.url.path.startswith(path) for path in protected_paths):
            try:
                token = self.extract_token(request)
                current_user = await get_current_user(token)
                request.state.user = current_user

                if request.url.path.startswith("/api/admin"):
                    await verify_admin(current_user)

            except HTTPException as e:
                return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
            except Exception as e:
                return JSONResponse(status_code=401, content={"detail": "Invalid token or insufficient permissions"})

        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    def extract_token(self, request: Request) -> str:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Authorization header missing")
        
        parts = auth_header.split()
        if parts[0].lower() != "bearer" or len(parts) != 2:
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        return parts[1]
