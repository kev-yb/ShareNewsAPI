from fastapi import FastAPI, APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(
    prefix = "/user",
    tags = ['Users']
)

# POSTs user credentials for sign up
@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = utils.hash_pwd(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# GETs news articles that a user saved to view/read later
@router.get('/savedlist', response_model = List[schemas.ArticleOut])
def view_saved_articles(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    saved_posts_list = current_user.id_saved_post
    saved_posts = []
    if len(saved_posts_list) == 0:
        return Response(status_code = status.HTTP_204_NO_CONTENT, detail = f"user's View Later list is empty")
    for post_id in saved_posts_list:
        post = db.query(models.Article).filter(models.Article.id == post_id).first()
        saved_posts.append(post)
    
    return saved_posts


# UPDATES view later list by deleting a specific news article for user with mentioned id
@router.patch('/savedlist/{post_id}', response_model = schemas.UserOut)
def delete_saved_article(post_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    saved_posts_list = current_user.id_saved_post
    if post_id not in saved_posts_list:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with {post_id} not found")
    index_post_id = saved_posts_list.index(post_id)
    saved_posts_list.pop(index_post_id)

    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user_query.update({"id_saved_post": saved_posts_list})

    article_query = db.query(models.Article).filter(models.Article.id == post_id)
    article = article_query.first()
    updated_saved_count = article.saved_count - 1
    article_query.update({"saved_count": updated_saved_count})
    
    db.commit()
    return user_query.first()
    


# GETs news articles shared to public by user with mentioned id
@router.get('/{user_id}', response_model = List[schemas.ArticleOut])
def user_articles(user_id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    user_articles = db.query(models.Article).filter(models.Article.user_id == user_id).all()
    if not user_articles:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"user's shared articles not found")
    return user_articles

