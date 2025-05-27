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