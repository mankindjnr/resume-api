from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, models, utils
from sqlalchemy.orm import Session
from ..database import get_db

from .. import schemas, models, utils, oauth2

router = APIRouter(
    tags=['Admin'],
)

@router.post('/admin', status_code=status.HTTP_201_CREATED, response_model=schemas.AdminResp)
def create_admin(admin: schemas.AdminBase, db: Session = Depends(get_db), the_admin: int = Depends(oauth2.get_current_admin)):
    admin.password = utils.hash_password(admin.password)

    new_admin = models.User(**admin.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {"Admin": [{"email": new_admin.email, "created_at": new_admin.created_at}]}

@router.get('/admin', status_code=status.HTTP_200_OK, response_model=schemas.AdminResp)
def get_admin(db: Session = Depends(get_db)):
    admin = db.query(models.User).filter(models.User.is_admin == True).first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Admin not found')

    return {"Admin": [{"email": admin.email, "created_at": admin.created_at}]}