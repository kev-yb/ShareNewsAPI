from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import database, models, schemas
from .config import settings

SECRET_ACCESS_TOKEN = f"{settings.secret_key}"
ALGORITHM = f"{settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expires_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expires": expire})
    encoded_jwt = jwt.encode(data, SECRET_ACCESS_TOKEN, ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
    detail = f"user's credentials are invalid", headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = jwt.decode(token, SECRET_ACCESS_TOKEN, algorithms = [ALGORITHM])
        user_id = payload["user_id"]

        if user_id is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"user's credentials with id {user_id} cannot be validated")

        user = db.query(models.User).filter(models.User.id == user_id).first()
        
        return user
      
    except JWTError:
        raise credentials_exception


