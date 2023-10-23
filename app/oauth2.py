from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings


oauth2_scheme =  OAuth2PasswordBearer(tokenUrl='login')
#SECRET_KEY
#Algorithm
#expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithms
ACCESS_TOKEN_EXPITRE_MINUTES = settings.access_token_expire_min

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPITRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=\
        status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials",
        headers={'www-Authenticate': "Bearer"})
    return verify_access_token(token, credentials_exception)