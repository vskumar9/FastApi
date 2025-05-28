from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from routers import user, auth, post, comment, like
# from config import settings
# from db import init_db  

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/about")
def about():
    return {"message": "This is the about page."}



@app.get("/blog")
def index(limit, published: bool = True):
    if published:
        return {'data': f'This is the blog page with limit {limit} and published posts.'}
    return {'data' : f'This is the blog page with limit {limit}.'}

@app.get("/blog/unpublished")
def unpublished():
    return {"message": "This is the unpublished blog page."}

@app.get("/blog/{id}")
def show(id: int):
    return {"ID": id}

@app.get("/blog/{id}/comment")
def comment(id):
    return {"message": "This is a comment."}