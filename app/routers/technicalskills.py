from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    tags=["Technical skills"],
)

@router.get("/technical-skills", response_model=schemas.TechnicalSkillsResp, status_code=status.HTTP_200_OK)
def get_all_technicalskills(db: Session = Depends(get_db)):
    all_skills = db.query(models.TechnicalSkills).all()

    skills_base = [schemas.TechnicalSkillsBase.from_orm(skills) for skills in all_skills]
    all_skills = schemas.TechnicalSkillsResp(TechnicalSkills=skills_base)
    return all_skills


@router.get("/technical-skills/{id}", response_model=schemas.TechnicalSkillsResp, status_code=status.HTTP_200_OK)
def get_technicalskills(id: int, db: Session = Depends(get_db)):
    skills = db.query(models.TechnicalSkills).filter(models.TechnicalSkills.id == id).first()

    if not skills:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Technical skills with id {id} not found")
    
    skills_resp = schemas.TechnicalSkillsBase.from_orm(skills)
    return schemas.TechnicalSkillsResp(TechnicalSkills=[skills_resp])


@router.post("/technical-skills", response_model=schemas.TechnicalSkillsResp, status_code=status.HTTP_201_CREATED)
def create_technical_skill(skills: schemas.TechnicalSkillsBase, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    new_skills = models.TechnicalSkills(**skills.dict())

    db.add(new_skills)
    db.commit()
    db.refresh(new_skills)

    skills_resp = schemas.TechnicalSkillsBase.from_orm(new_skills)
    return schemas.TechnicalSkillsResp(TechnicalSkills=[skills_resp])

@router.put("/technical-skills/{id}", response_model=schemas.TechnicalSkillsResp, status_code=status.HTTP_202_ACCEPTED)
def update_technical_skills(id: int, technical_skill: schemas.TechnicalSkillsBase, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    skills_to_update = db.query(models.TechnicalSkills).filter(models.TechnicalSkills.id == id).first()

    if not skills_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Technical skills with id {id} not found")
    
    update_data = technical_skill.dict(exclude_unset=True)
    db.query(models.TechnicalSkills).filter(models.TechnicalSkills.id == id).update(update_data, synchronize_session=False)
    db.commit()

    updated_skills = schemas.TechnicalSkillsBase.from_orm(skills_to_update)
    return schemas.TechnicalSkillsResp(TechnicalSkills=[updated_skills])

@router.delete("/technical-skills/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_technical_skills(id: int, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    skills_to_delete = db.query(models.TechnicalSkills).filter(models.TechnicalSkills.id == id).first()

    if not skills_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Technical skills with id {id} not found")
    
    db.query(models.TechnicalSkills).filter(models.TechnicalSkills.id == id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)