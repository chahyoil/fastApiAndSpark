from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# 이 값들은 실제 운영 환경에서는 환경 변수 등으로 안전하게 관리해야 합니다.
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str = ""  # Make it optional with a default empty string

# 비밀번호 해싱
def get_password_hash(password):
    return pwd_context.hash(password)

# 비밀번호 검증
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 토큰 생성
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 토큰 검증
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        # Here, you should fetch the user from your database and include the is_admin field
        user = {"username": username, "is_admin": False}  # Placeholder, replace with actual user data
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

# 관리자 권한 확인
async def verify_admin(current_user: User = Depends(get_current_user)):
    if current_user.username != "admin":
        raise HTTPException(status_code=400, detail="Not an admin user")