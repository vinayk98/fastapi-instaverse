from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.models import Db_user
from routers.schemas import UserBase
from db.hash import Hash

def create_user(db: Session, request: UserBase):
    new_user = Db_user(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str):
    user = db.query(Db_user).filter(Db_user.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with this username {username} not found") 
    return user
 