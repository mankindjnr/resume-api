from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    tags=["Work Experience"],
)

@router.get("/work-experience", response_model=schemas.workResp, status_code=status.HTTP_200_OK)
def get_work_experience(db: Session = Depends(get_db)):
    all_experience = db.query(models.WorkExperience).all()

    experience_base = [schemas.workBase.from_orm(experience) for experience in all_experience]
    all_experience_resp = schemas.workResp(WorkExperience=experience_base)
    return all_experience_resp


@router.get("/work-experience/{id}", response_model=schemas.workResp, status_code=status.HTTP_200_OK)
def get_work_experience(id: int, db: Session = Depends(get_db)):
    experience = db.query(models.WorkExperience).filter(models.WorkExperience.id == id).first()

    if not experience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Work Experience with id {id} not found")
    
    experience_resp = schemas.workBase.from_orm(experience)
    return schemas.workResp(WorkExperience=[experience_resp])


@router.post("/work-experience", response_model=schemas.workResp, status_code=status.HTTP_201_CREATED)
def create_work_experience(experience: schemas.workBase, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    new_experience = models.WorkExperience(**experience.dict())

    db.add(new_experience)
    db.commit()
    db.refresh(new_experience)

    experience_resp = schemas.workBase.from_orm(new_experience)
    return schemas.workResp(WorkExperience=[experience_resp])


@router.put("/work-experience/{id}", response_model=schemas.workResp, status_code=status.HTTP_202_ACCEPTED)
def update_work_experience(id: int, experience: schemas.workBase, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    experience_to_update = db.query(models.WorkExperience).filter(models.WorkExperience.id == id).first()

    if not experience_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Work Experience with id {id} not found")
    
    update_data = experience.dict(exclude_unset=True)
    db.query(models.WorkExperience).filter(models.WorkExperience.id == id).update(update_data, synchronize_session=False)
    db.commit()

    updated_experience = schemas.workBase.from_orm(experience_to_update)
    return schemas.workResp(WorkExperience=[updated_experience])


@router.delete("/work-experience/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_experience(id: int, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    experience_to_delete = db.query(models.WorkExperience).filter(models.WorkExperience.id == id).first()

    if not experience_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Work Experience with id {id} not found")
    
    db.delete(experience_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)