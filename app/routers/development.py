from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from .. import schemas, models

router = APIRouter(
    tags=["Development"],
)


@router.get("/development", response_model=schemas.DevelopmentResp, status_code=status.HTTP_200_OK)
def get_all_development(db: Session = Depends(get_db)):
    all_development = db.query(models.Development).all()

    development_base = [schemas.DevelopmentBase.from_orm(development) for development in all_development]
    all_development = schemas.DevelopmentResp(Development=development_base)
    return all_development

@router.get("/development/{id}", response_model=schemas.DevelopmentResp, status_code=status.HTTP_200_OK)
def get_development(id: int, db: Session = Depends(get_db)):
    development = db.query(models.Development).filter(models.Development.id == id).first()

    if not development:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Development with id {id} not found")
    
    development_resp = schemas.DevelopmentBase.from_orm(development)
    return schemas.DevelopmentResp(Development=[development_resp])

@router.post("/development", response_model=schemas.DevelopmentResp, status_code=status.HTTP_201_CREATED)
def create_development(development: schemas.DevelopmentBase, db: Session = Depends(get_db)):
    new_development = models.Development(**development.dict())

    db.add(new_development)
    db.commit()
    db.refresh(new_development)

    development_resp = schemas.DevelopmentBase.from_orm(new_development)
    return schemas.DevelopmentResp(Development=[development_resp])

@router.put("/development/{id}", response_model=schemas.DevelopmentResp, status_code=status.HTTP_202_ACCEPTED)
def update_development(id: int, development: schemas.DevelopmentBase, db: Session = Depends(get_db)):
    development_to_update = db.query(models.Development).filter(models.Development.id == id).first()

    if not development_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Development with id {id} not found")
    
    update_data = development.dict(exclude_unset=True)
    db.query(models.Development).filter(models.Development.id == id).update(update_data, synchronize_session=False)
    db.commit()

    updated_development = schemas.DevelopmentBase.from_orm(development_to_update)
    return schemas.DevelopmentResp(Development=[updated_development])

@router.delete("/development/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_development(id: int, db: Session = Depends(get_db)):
    development_to_delete = db.query(models.Development).filter(models.Development.id == id).first()

    if not development_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Development with id {id} not found")
    
    db.query(models.Development).filter(models.Development.id == id).delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)