from os import access
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import List
from pydantic import utils
from sqlalchemy.orm import Session
from .. import oauth2, schemas, models, utils
from ..database import get_db



router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    userfound = db.query(models.User).filter(models.User.email == user.username).first()

    if not userfound:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid credential",
        )
    if not utils.verify(user.password, userfound.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credential"         
        )
        
    access_token = oauth2.create_access_token(dict({"user_id" : userfound.id}))

    return {"access_token" : access_token, "token_type": "bearer"}
