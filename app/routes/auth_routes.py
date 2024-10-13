from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from utils.auth import (
    Token, User, verify_password, create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
)

router = APIRouter()

# 임시 사용자 데이터베이스 (실제 구현에서는 데이터베이스를 사용해야 합니다)
fake_users_db = {
    "testuser": User(
        username="testuser",
        full_name="Test User",
        email="testuser@example.com",
        hashed_password=get_password_hash("testpassword"),
        disabled=False,
    ).dict(),
    "admin": User(
        username="admin",
        full_name="Admin User",
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        disabled=False,
    ).dict(),
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)
    return None

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}