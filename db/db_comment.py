
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.models import Db_comment, Db_post
from routers.schemas import CommentBase, PostBase
import datetime

def create(db: Session, request: CommentBase):
    new_comment = Db_comment(
        text=request.text,
        username=request.username,
        post_id=request.post_id,
        timestamp=datetime.datetime.now(),
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_all(db: Session, post_id: int):
    return db.query(Db_comment).filter(Db_comment.id == post_id).all()
    