from fastapi import FastAPI, APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List

router = APIRouter(
    prefix = "/news",
    tags = ['News']
)

# GETs user all news available on the website
@router.get('/')
def get_articles():
    pass

# POSTs news article
@router.post('/')
def post_article():
    pass

# GETs news article with mentioned id
@router.get('/{id}')
def get_article():
    pass

# DELETEs news article with mentioned id
@router.delete('/{id}')
def delete_article():
    pass

# UPDATEs news article with mentioned id
@router.put('/{id}')
def update_article():
    pass

# POSTs news article with mentioned id to user's "view later" page
@router.post('/{id}')
def save_article():
    pass

# POST: allows users to like a news article with mentioned id
@router.post('/{id}/vote')
def like_article():
    pass
