from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, models, utils
from sqlalchemy.orm import Session
from ..database import get_db

from .. import schemas, models, utils, oauth2

router = APIRouter(
    tags=['Users'],
)

@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResp)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    user.password = utils.hash_password(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"User": [{"email": new_user.email, "created_at": new_user.created_at}]}

@router.get('/users', status_code=status.HTTP_200_OK, response_model=schemas.UserResp)
def get_user(db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    all_users = db.query(models.User).all()

    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No users found')

    return {"User": [{"email": user.email, "created_at": user.created_at} for user in all_users]}