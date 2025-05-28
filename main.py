from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
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
def index(limit : int = 10, published: bool = True, sort: Optional[str] = None): #Optional arguments are disregarded when no data is provided.
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

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

    pass

@app.post("/blog")
def create_blog(request: Blog):
    return {"message": f"Blog is created with title as {request.title}"}


# if __name__ == '__main__':
#     uvicorn.run(app, host="127.0.0.1", port=9000)