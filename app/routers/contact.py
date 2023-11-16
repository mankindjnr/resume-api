from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    tags=["Contact"],
)

@router.get('/contacts', response_model=schemas.ContactResp, status_code=status.HTTP_200_OK)
def get_all(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    contact_base = [schemas.ContactBase.from_orm(contact) for contact in contacts]
    contacts = schemas.ContactResp(SoftwareEngineer=contact_base)
    return contacts

@router.post('/contacts', response_model=schemas.ContactResp, status_code=status.HTTP_201_CREATED)
def add_contact(contact: schemas.ContactBase, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    new_contact = models.Contact(**contact.dict())

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    contact_resp = schemas.ContactBase.from_orm(new_contact)
    return schemas.ContactResp(SoftwareEngineer=[contact_resp])

@router.put('/contacts/{id}', response_model=schemas.ContactResp, status_code=status.HTTP_202_ACCEPTED)
def update_contacts(id: int, contact: schemas.ContactBase, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    contact_to_update = db.query(models.Contact).filter(models.Contact.id == id).first()

    if not contact_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id {id} not found")
    
    update_data = contact.dict(exclude_unset=True)
    db.query(models.Contact).filter(models.Contact.id == id).update(update_data, synchronize_session=False)
    db.commit()

    updated_contact = schemas.ContactBase.from_orm(contact_to_update)
    return schemas.ContactResp(SoftwareEngineer=[updated_contact])

@router.delete('/contacts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(id: int, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    contact_to_delete = db.query(models.Contact).filter(models.Contact.id == id).first()

    if not contact_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id {id} not found")
    
    db.delete(contact_to_delete)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)