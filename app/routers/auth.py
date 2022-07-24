from fastapi import FastAPI, APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List

router = APIRouter(
    prefix = "/auth",
    tags = ['Authorization']
)

# POSTs users credentials and facilitates login
@router.post('/login')
def login():
    pass