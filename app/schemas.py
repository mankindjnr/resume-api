from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from pydantic.types import conint

# ====================  Summary  ====================
class SummaryBase(BaseModel):
    summary: List[str]

    class Config:
        orm_mode = True
        from_attributes = True

class SummaryResp(BaseModel):
    Summary: List[SummaryBase]

    class Config:
        orm_mode = True

# ====================  Education  ====================
class EducationBase(BaseModel):
    school: str
    location: str
    degree: str
    start_date: str
    end_date: str

    class Config:
        orm_mode = True
        from_attributes = True

class EducationResp(BaseModel):
    Education: List[EducationBase]

    class Config:
        orm_mode = True

class EducationUpdate(BaseModel):
    school: Optional[str]
    location: Optional[str]
    degree: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]

    class Config:
        orm_mode = True
        from_attributes = True

# ====================  Work Experience  ====================
class workBase(BaseModel):
    company: str
    location: str
    position: str
    info: List[str]
    start_date: str
    end_date: str

    class Config:
        orm_mode = True
        from_attributes = True

class workResp(BaseModel):
    WorkExperience: List[workBase]

    class Config:
        orm_mode = True

# ====================  Development  ====================
class DevelopmentBase(BaseModel):
    skill: str
    institution: str
    location: str
    info: List[str]
    start_date: str
    end_date: str

    class Config:
        orm_mode = True
        from_attributes = True

class DevelopmentResp(BaseModel):
    Development: List[DevelopmentBase]

    class Config:
        orm_mode = True

# ====================  Technical Skills  ====================
class TechnicalSkillsBase(BaseModel):
    languages: List[str]
    development_frameworks: List[str]
    version_control: List[str]
    containerization: List[str]
    dbms: List[str]
    BaaS_platform: List[str]
    cloud_platform: List[str]
    others: List[str]

    class Config:
        orm_mode = True
        from_attributes = True

class TechnicalSkillsResp(BaseModel):
    TechnicalSkills: List[TechnicalSkillsBase]

    class Config:
        orm_mode = True

# ====================  Projects  ====================
class ProjectsBase(BaseModel):
    title: str
    description: str
    link: str

    class Config:
        orm_mode = True
        from_attributes = True

class ProjectsResp(BaseModel):
    Projects: List[ProjectsBase]

    class Config:
        orm_mode = True

# ====================  Contact  ====================
class ContactBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    x: str
    linkedin: str
    github: str
    website: str

    class Config:
        orm_mode = True
        from_attributes = True

class ContactResp(BaseModel):
    SoftwareEngineer: List[ContactBase]

    class Config:
        orm_mode = True

# ====================  RESUME  ====================
class ResumeResp(BaseModel):
    Summary: List[SummaryBase]
    Education: List[EducationBase]
    WorkExperience: List[workBase]
    Development: List[DevelopmentBase]
    TechnicalSkills: List[TechnicalSkillsBase]
    Projects: List[ProjectsBase]
    SoftwareEngineer: List[ContactBase]

    class Config:
        orm_mode = True

# ====================  User  ====================