from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from auth.oauth2 import get_current_user
from db import db_post
import string
import shutil
import random
from db.database import get_db
from routers.schemas import PostBase, PostDisplay, UserAuth

router = APIRouter(
    prefix="/post",
    tags=["post"]
)
image_url_types = ["absolute", "relative"]

@router.post("/new", response_model=PostDisplay)    
def create_new_post(
    request: PostBase,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user)
):
    if request.image_url_type not in image_url_types:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='parameter image_url_type can only take values "absolute" or "relative"'
        )
    return db_post.create(db, request)

@router.get("/all", response_model=list[PostDisplay])
def get_all_posts(db: Session = Depends(get_db)):
    return db_post.get_all(db)

@router.post("/image") 
def upload_image(image: UploadFile, current_user: UserAuth = Depends(get_current_user)):
    letter = string.ascii_letters
    rand_str= " ".join(random.choice(letter) for i in range(6))
    new = f"_{rand_str}."
    filename = new.join(image.filename.rsplit(".", 1))
    path = f"images/{filename}"

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {
        'filename': path
    }
    
@router.delete("/delete/{id}")
def delete(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_post.delete_post(db, id, current_user.id)

@router.get("/user")
def get_user_posts(
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user)
):
    return db_post.get_user_posts(
        db,
        current_user.id
    )
    
@router.get("/{id}", response_model=PostDisplay)
def get_user_post_with_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user)
):
    post = db_post.get_post(db, id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post