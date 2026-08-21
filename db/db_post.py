from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.models import Db_post
from routers.schemas import PostBase
import datetime

def create(db: Session, request: PostBase):
    new_post = Db_post(
        image_url=request.image_url,
        image_url_type=request.image_url_type,
        caption=request.caption,
        timestamp=datetime.datetime.now(),
        user_id=request.creator_id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_all(db: Session):
    return (
        db.query(Db_post)
        .order_by(Db_post.timestamp.desc())
        .all()
    )
    
def get_post(db: Session, id: int):
    return db.query(Db_post).filter(
        Db_post.id == id
    ).first()

def delete_post(db: Session, id: int, user_id: int):
    post = db.query(Db_post).filter(Db_post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with this id {id} not found")
    if post.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"only post creator delete the post")
    else:
        db.delete(post)
        db.commit()
        return {"message": "post deleted successfully"}
    
def get_user_posts(db: Session, user_id: int):

    posts = (
        db.query(Db_post)
        .filter(Db_post.user_id == user_id)
        .all()
    )

    return posts