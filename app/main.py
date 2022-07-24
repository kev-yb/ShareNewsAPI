from fastapi import FastAPI
from .routers import auth, news, user

app = FastAPI()

app.include_router(news.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return {"message": "Welcome to ShareNewsAPI"}