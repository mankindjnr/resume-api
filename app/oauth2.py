from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from decouple import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

SECRET_KEY = config("JWT_SECRET")
ALGORITHM = config("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("JWT_EXPIRE_MINUTES")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=str(id))

    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "invalid credentials", headers="WWW-Authenticate: Bearer")

    token = verify_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "invalid credentials", headers="WWW-Authenticate: Bearer")

    token = verify_token(token, credentials_exception)

    admin = db.query(models.User).filter(models.User.id == token.id).first()

    if not admin.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'You are not an admin')

    return admin
