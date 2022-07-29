from tkinter import CASCADE
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, text, ARRAY
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key = True, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete=CASCADE), nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))
    article_url = Column(String, nullable = False)
    article_title = Column(String, nullable = False)
    article_author = Column(String, nullable = True)
    article_content = Column(String, nullable = True)
    saved_count = Column(Integer, nullable = False, server_default = text('0'))
    user = relationship('User')

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    id_saved_post = Column(ARRAY(Integer), nullable = False, default = {})


