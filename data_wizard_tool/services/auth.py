from datetime import datetime, timedelta

from authlib.jose import JoseError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from data_wizard_tool.config.config import ALGORITHM, SECRET_KEY
from data_wizard_tool.database import get_db
from data_wizard_tool.schemas.user import UserCreateSchema
from data_wizard_tool.models.user import User
from data_wizard_tool.utils.auth_utils import (get_password_hash,
                                               verify_password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    header = {'alg': ALGORITHM}
    encoded_jwt = jwt.encode(header, to_encode, SECRET_KEY)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":
                 "Bearer"},
    )
    try:
        payload = jwt.decode(token,
                             SECRET_KEY)
        # IMPORTANT: Verify the token
        # This is usually done by checking if the token is revoked, expired, etc.
        # Here, we just check if the username is in the payload
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JoseError as e:
        print(e)
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_user(db: Session, user: UserCreateSchema):
    # Hash the password
    hashed_password = get_password_hash(user.password)
    # Create a new user instance with the hashed password
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
