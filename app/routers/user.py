from fastapi import FastAPI, APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/user",
    tags = ['Users']
)

# POSTs user credentials for sign up
@router.post('/')
def sign_up():
    pass

# GETs news articles shared to public by user with mentioned id
@router.get('/{user_id}')
def user_articles():
    pass

# GETs news articles that a user saved to view/read later
@router.get('/{user_id}/savedlist')
def view_saved_articles():
    pass

# DELETEs a specific news article from view later page of user with mentioned id
@router.delete('/{id}/savedlist/{post_id}')
def delete_saved_article():
    pass