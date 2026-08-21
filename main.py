from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import models
from db.database import engine
from fastapi.staticfiles import StaticFiles
from routers import user
from routers import post
from routers import comment
from auth import authentication
app = FastAPI() 

@app.get("")
def get_message():
    return "Hello world"

app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(authentication.router)
models.Base.metadata.create_all(engine) 
#create the database tables based on the models defined in db/models.py
origins = ["http://localhost:3000", "https://blogs-five-tan.vercel.app"] #define the allowed origins for CORS (Cross-Origin Resource Sharing) requests
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]) #add CORS middleware to the application
# app.mount("/images", StaticFiles(directory="images"), name="images")
