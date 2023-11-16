from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas, database, models, utils, oauth2

router = APIRouter(
    tags = ['Authentication']
)

@router.post('/signin', response_model=schemas.Token)
def signin(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f'Invalid Credentials')

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f'Incorrect Password')

    access_token = oauth2.create_access_token(data={"user_id": user.id, "email": user.email, "role": "user"})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signin/admin", response_model=schemas.Token)
def admin_login(admin_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    admin = db.query(models.User).filter(models.User.email == admin_credentials.username).first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f'Invalid Credentials')

    if not utils.verify_password(admin_credentials.password, admin.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f'Incorrect Credentials')
    
    if not admin.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Not an admin')

    access_token = oauth2.create_access_token(data={"user_id": admin.id, "email": admin.email, "role": "admin" })
    return {"access_token": access_token, "token_type": "bearer"}