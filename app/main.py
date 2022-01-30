from fastapi import FastAPI
from database import engine, Base
from routers import users, posts, oauth, votes

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(users.router, prefix="/user")
app.include_router(posts.router, prefix="/post")
app.include_router(votes.router, prefix="/vote")
app.include_router(oauth.router)


@app.get('/')
def root():
    return {"message": "Hello World"}
