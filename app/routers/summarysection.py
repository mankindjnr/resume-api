from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from .. import schemas, models

router = APIRouter(
    tags=["sections"],
)

@router.get("/summary", response_model=schemas.Summary, status_code=status.HTTP_200_OK)
def summary():
    return {"SUMMARY": "mankindjnr resume to the World"}

@router.post("/summary", response_model=schemas.SummaryBase, status_code=status.HTTP_201_CREATED)
def create_summary(summary: schemas.SummaryBase, db: Session = Depends(get_db)):
    new_summary = models.Summary(**summary.dict())

    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    return new_summary

@router.put("/summary", response_model=schemas.SummaryBase, status_code=status.HTTP_202_ACCEPTED)
def update_summary():
    return {"SUMMARY": "mankindjnr resume to the World"}