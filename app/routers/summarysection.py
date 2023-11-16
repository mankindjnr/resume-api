from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from .. import schemas, models, utils, oauth2
from ..models import User

router = APIRouter(
    tags=["SUMMARY"],
)
# remember with the current_user/admin dependance, you can pull the user/admin currently logged in form it

@router.get("/summary", response_model=schemas.SummaryResp, status_code=status.HTTP_200_OK)
def summary(db: Session = Depends(get_db)):
    all_summary = db.query(models.Summary).all()

    # convert list of dict to list of SummaryResponse instances
    summary_base = [schemas.SummaryBase.from_orm(summary) for summary in all_summary]
    all_summary_resp = schemas.SummaryResp(Summary=summary_base)
    return all_summary_resp

@router.post("/summary", response_model=schemas.SummaryResp, status_code=status.HTTP_201_CREATED)
def create_summary(summary: schemas.SummaryBase, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    new_summary = models.Summary(**summary.dict())

    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)

    summary_resp = schemas.SummaryBase.from_orm(new_summary)
    return schemas.SummaryResp(Summary=[summary_resp])

@router.put("/summary/{id}", response_model=schemas.SummaryBase, status_code=status.HTTP_202_ACCEPTED)
def update_summary(id: int, summary: schemas.SummaryBase, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    summary_update = db.query(models.Summary).filter(models.Summary.id == id).first()

    if not summary_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Summary with id {id} not found")
    
    update_summary = summary.dict(exclude_unset=True)
    db.query(models.Summary).filter(models.Summary.id == id).update(update_summary, synchronize_session=False)
    db.commit()

    updated_summary = schemas.SummaryBase.from_orm(summary_update)
    return schemas.SummaryResp(Summary=[updated_summary])


@router.delete("/summary/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_summary(id: int, db: Session = Depends(get_db), admin: int = Depends(oauth2.get_current_admin)):
    summary_to_delete = db.query(models.Summary).filter(models.Summary.id == id).first()

    if not summary_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Summary with id {id} not found")
    
    db.delete(summary_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
