import jwt
from jwt.exceptions import InvalidTokenError

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from app import schemas, database, models
from app.config import settings

from datetime import datetime, timedelta

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str,  credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_obtained = payload.get("id")
        type_user_obtained = payload.get("type_user")
        print(f"verify id = {id_obtained}, type_user = {type_user_obtained}")
        if id_obtained is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id_obtained, type_user=type_user_obtained)
    except InvalidTokenError:
        raise credentials_exception
    return token_data
def get_current_general(token: str=Depends(oauth2), db: Session=Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credentials_exception)
    return token
def get_current_elector(token: str = Depends(oauth2), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credentials_exception)
    if token.type_user != "elector":
        raise credentials_exception
    return token
def get_current_admin(token: str = Depends(oauth2), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credentials_exception)
    if token.type_user != "admin":
        raise credentials_exception
    return token
