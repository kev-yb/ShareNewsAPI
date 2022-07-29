from fastapi import FastAPI, APIRouter, Response, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import database, models, schemas, utils, oauth2

router = APIRouter(tags = ['Authentication'])

# POSTs users credentials and facilitates login
@router.post('/login', status_code = status.HTTP_202_ACCEPTED, response_model = schemas.TokenOut)
def login(userform: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == userform.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"User credentials are invalid")
    
    verification = utils.verify_pwd(userform.password, user.password)
    if not verification:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"User credentials are invalid")
    
    access_token = oauth2.create_access_token({"user_id": user.id, "user_email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}