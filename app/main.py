from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from sqlalchemy.orm import Session

from .routers import summarysection, educationsection, workexperience, development, technicalskills, projects, contact
from . import schemas, models, database
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=schemas.ResumeResp, status_code=200)
def resume(db: Session = Depends(database.get_db)):
    all_summary = db.query(models.Summary).all()
    all_education = db.query(models.Education).all()
    all_work_experience = db.query(models.WorkExperience).all()
    all_development = db.query(models.Development).all()
    all_technical_skills = db.query(models.TechnicalSkills).all()
    all_projects = db.query(models.Projects).all()
    all_contact = db.query(models.Contact).all()
    
    summary_base = [schemas.SummaryBase.from_orm(summary) for summary in all_summary]
    education_base = [schemas.EducationBase.from_orm(education) for education in all_education]
    work_experience_base = [schemas.workBase.from_orm(work) for work in all_work_experience]
    development_base = [schemas.DevelopmentBase.from_orm(development) for development in all_development]
    technical_skills_base = [schemas.TechnicalSkillsBase.from_orm(technical_skills) for technical_skills in all_technical_skills]
    projects_base = [schemas.ProjectsBase.from_orm(projects) for projects in all_projects]
    contact_base = [schemas.ContactBase.from_orm(contact) for contact in all_contact]

    all_resume = schemas.ResumeResp(Summary=summary_base, Education=education_base, WorkExperience=work_experience_base, Development=development_base, TechnicalSkills=technical_skills_base, Projects=projects_base, SoftwareEngineer=contact_base)
    return all_resume

app.include_router(summarysection.router)
app.include_router(educationsection.router)
app.include_router(workexperience.router)
app.include_router(development.router)
app.include_router(technicalskills.router)
app.include_router(projects.router)
app.include_router(contact.router)