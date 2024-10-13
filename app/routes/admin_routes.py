from utils.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.get("/admin-only-endpoint")
async def admin_only_endpoint(current_user: dict = Depends(get_current_user)):
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this endpoint"
        )
    return {"message": "Welcome, admin!"}

@router.get("/protected")
async def protected_function(current_user: dict = Depends(get_current_user)):
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this endpoint"
        )
    return {"message": "This is a protected function"}