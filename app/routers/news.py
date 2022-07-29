from fastapi import FastAPI, APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix = "/news",
    tags = ['News']
)

# GETs all news available on the website
@router.get('/', response_model = List[schemas.ArticleOut])
def get_articles(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    articles = db.query(models.Article).all()
    return articles


# POSTs news article
@router.post('/', response_model = schemas.ArticleOut)
def post_article(article: schemas.ArticleBase, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    article = models.Article(user_id = current_user.id, **article.dict())
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


# UPDATEs user profile by adding news article with mentioned id to user's "view later" page
@router.patch('/save/{id}', response_model = schemas.UserOut)
def save_article(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    article_query = db.query(models.Article).filter(models.Article.id == id)
    article = article_query.first()
    saved_list = current_user.id_saved_post
    if id in saved_list:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"post with id {id} already saved")
    saved_list.append(id)

    if not article:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")
    user_query.update({"id_saved_post": saved_list}, synchronize_session=False)
    updated_saved_count = article.saved_count + 1
    article_query.update({"saved_count": updated_saved_count})
    db.commit()
    return user_query.first()


# GETs news article with mentioned id
@router.get('/{id}', response_model = schemas.ArticleOut)
def get_article(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    article = db.query(models.Article).filter(models.Article.id == id).first()
    if not article:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")
    return article


# DELETEs news article with mentioned id
@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_article(id: int, db: Session =  Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    article_query = db.query(models.Article).filter(models.Article.id == id)
    article = article_query.first()
    
    if not article:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")
    if article.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not allowed to delete user {article.user_id}'s post")
    
    article_query.delete(synchronize_session=False)
    db.commit()


# UPDATEs news article with mentioned id
@router.put('/{id}', response_model = schemas.ArticleOut)
def update_article(id: int, info: dict, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    article_query = db.query(models.Article).filter(models.Article.id == id)
    article = article_query.first()

    if not article:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")
    if article.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not allowed to update user {current_user.id}'s post")
    
    article_query.update(info, synchronize_session = False)
    db.commit()
    return article_query.first()
    