from fastapi import FastAPI
from .database import engine, Base
from .routers import users, posts, oauth, votes
from fastapi.middleware.cors import CORSMiddleware

# Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router, prefix="/user")
app.include_router(posts.router, prefix="/post")
app.include_router(votes.router, prefix="/vote")
app.include_router(oauth.router)


@app.get('/')
def root():
    return {"message": "Hello World"}
