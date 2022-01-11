from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm.session import Session
from .config import settings

from starlette import status

from app import models
from . import schemas, database
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def verify_access_token(token: str, credential_exception):

    try:

        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        id: str = payload.get("user_id")

        if id is None:
            raise credential_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    tokenreturn = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == tokenreturn.id).first()

    if not user:
        raise credential_exception

    return user
