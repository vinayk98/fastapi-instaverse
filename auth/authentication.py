from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.oauth2 import create_access_token
from db.database import get_db
from db.hash import Hash
from db.models import Db_user

router = APIRouter(
    prefix="/login",
    tags=["login"]
)
@router.post("")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = (
        db.query(Db_user)
        .filter(Db_user.username == request.username)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = create_access_token(data={"username": user.username})
    return{
        "access_token": access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }
    
