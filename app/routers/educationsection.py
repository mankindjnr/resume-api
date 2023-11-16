from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    tags=["EDUCATION"],
)

@router.get("/education", response_model=schemas.EducationResp, status_code=status.HTTP_200_OK)
def education(db: Session = Depends(get_db)):
    all_education = db.query(models.Education).all()

    # convert list of dict to list of EducationResponse instances
    education_base = [schemas.EducationBase.from_orm(edu) for edu in all_education]
    all_education_resp = schemas.EducationResp(Education=education_base)
    return all_education_resp

@router.get("/education/{id}", response_model=schemas.EducationResp, status_code=status.HTTP_200_OK)
def education(id: int, db: Session = Depends(get_db)):
    education = db.query(models.Education).filter(models.Education.id == id).first()

    if not education:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Education with id {id} not found")
    
    education_resp = schemas.EducationBase.from_orm(education)
    return schemas.EducationResp(Education=[education_resp])


@router.post("/education", response_model=schemas.EducationResp, status_code=status.HTTP_201_CREATED)
def education(education: schemas.EducationBase, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    new_education = models.Education(**education.dict())

    db.add(new_education)
    db.commit()
    db.refresh(new_education)

    education_resp = schemas.EducationBase.from_orm(new_education)
    return schemas.EducationResp(Education=[education_resp])


@router.put("/education/{id}", response_model=schemas.EducationResp, status_code=status.HTTP_202_ACCEPTED)
def update_education(id: int, education: schemas.EducationBase, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    education_to_update = db.query(models.Education).filter(models.Education.id == id).first()

    if not education_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Education with id {id} not found")
    
    update_data = education.dict(exclude_unset=True)
    db.query(models.Education).filter(models.Education.id == id).update(update_data, synchronize_session=False)
    db.commit()

    updated_education = schemas.EducationBase.from_orm(education_to_update)
    return schemas.EducationResp(Education=[updated_education])

@router.delete("/education/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education(id: int, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    education_to_delete = db.query(models.Education).filter(models.Education.id == id).first()

    if not education_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Education with id {id} not found")
    
    db.query(models.Education).filter(models.Education.id == id).delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)





"""
#We could not use patch since our db requires all fields to be filled, so we use put instead

@router.put("/education/{id}", response_model=schemas.EducationResp, status_code=status.HTTP_202_ACCEPTED)
def update_education(id: int, education: schemas.EducationUpdate, db: Session = Depends(get_db)):
    education_bullet = db.query(models.Education).filter(models.Education.id == id)
    education_to_update = education_bullet.first()

    if not education_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Education with id {id} not found")
    
    update_data = education.dict(exclude_unset=True)
    education_bullet.update(education.dict(), synchronize_session=False)
    db.commit()

    bullet_resp = schemas.EducationUpdate.from_orm(education_bullet.first())
    return schemas.EducationResp(Education=[bullet_resp])
"""