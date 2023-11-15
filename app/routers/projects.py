from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from .. import schemas, models

router = APIRouter(
    tags=["Projects"],
)

@router.get("/projects", response_model=schemas.ProjectsResp, status_code=status.HTTP_200_OK)
def get_all_projects(db: Session = Depends(get_db)):
    all_projects = db.query(models.Projects).all()

    projects_base = [schemas.ProjectsBase.from_orm(projects) for projects in all_projects]
    all_projects = schemas.ProjectsResp(Projects=projects_base)
    return all_projects

@router.get("/projects/{id}", response_model=schemas.ProjectsResp, status_code=status.HTTP_200_OK)
def get_a_project(id: int, db: Session =  Depends(get_db)):
    project = db.query(models.Projects).filter(models.Projects.id == id).first()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found")
    
    project_resp = schemas.ProjectsBase.from_orm(project)
    return schemas.ProjectsResp(Projects=[project_resp])

@router.post("/projects", response_model=schemas.ProjectsResp, status_code=status.HTTP_201_CREATED)
def add_project(project: schemas.ProjectsBase, db: Session = Depends(get_db)):
    new_project = models.Projects(**project.dict())

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    project_resp = schemas.ProjectsBase.from_orm(new_project)
    return schemas.ProjectsResp(Projects=[project_resp])

@router.put("/projects/{id}", response_model=schemas.ProjectsResp, status_code=status.HTTP_202_ACCEPTED)
def update_project(id: int, project: schemas.ProjectsBase, db: Session = Depends(get_db)):
    project_to_update = db.query(models.Projects).filter(models.Projects.id == id).first()

    if not project_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found")
    
    update_data = project.dict(exclude_unset=True)
    db.query(models.Projects).filter(models.Projects.id == id).update(update_data, synchronize_session=False)
    db.commit()

    updated_project = schemas.ProjectsBase.from_orm(project_to_update)
    return schemas.ProjectsResp(Projects=[updated_project])

@router.delete("/projects/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int, db: Session = Depends(get_db)):
    project_to_delete = db.query(models.Projects).filter(models.Projects.id == id).first()

    if not project_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {id} not found")
    
    db.query(models.Projects).filter(models.Projects.id == id).delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
