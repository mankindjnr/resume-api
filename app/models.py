from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, text, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
import datetime
import json
from sqlalchemy.dialects.postgresql import JSONB

class Summary(Base):
    __tablename__ = 'summary'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    summary = Column(JSONB, nullable=False)

class Education(Base):
    __tablename__ = 'education'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    school = Column(String(60), nullable=False)
    location = Column(String(30), nullable=False)
    degree = Column(String(40), nullable=False)
    start_date = Column(String(30), nullable=False)
    end_date = Column(String(30), nullable=False)

class WorkExperience(Base):
    __tablename__ = 'work_experience'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    company = Column(String(60), nullable=False)
    location = Column(String(30), nullable=False)
    position = Column(String(40), nullable=False)
    info = Column(JSONB, nullable=False)
    start_date = Column(String(30), nullable=False)
    end_date = Column(String(30), nullable=False)

    def set_info(self, info_list):
        self.info = info_list

    def get_info(self):
        return self.info

class Development(Base):
    __tablename__ = 'development'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    skill = Column(String(60), nullable=False)
    institution = Column(String(60), nullable=False)
    location = Column(String(30), nullable=False)
    info = Column(JSONB, nullable=False)
    start_date = Column(String(30), nullable=False)
    end_date = Column(String(30), nullable=False)

    def set_info(self, info_list):
        self.info = info_list
    
    def get_info(self):
        return self.info

class TechnicalSkills(Base):
    __tablename__ = 'technical_skills'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    languages = Column(JSONB, nullable=False)
    development_frameworks = Column(JSONB, nullable=False)
    version_control = Column(JSONB, nullable=False)
    containerization = Column(JSONB, nullable=False)
    dbms = Column(JSONB, nullable=False)
    BaaS_platform = Column(JSONB, nullable=False)
    cloud_platform = Column(JSONB, nullable=False)
    others = Column(JSONB, nullable=False)

    def set_languages(self, languages_list):
        self.languages = languages_list

    def get_languages(self):
        return self.languages

    def set_development_frameworks(self, development_frameworks_list):
        self.development_frameworks = development_frameworks_list

    def get_development_frameworks(self):
        return self.development_frameworks

    def set_version_control(self, version_control_list):
        self.version_control = version_control_list

    def get_version_control(self):
        return self.version_control

    def set_containerization(self, containerization_list):
        self.containerization = containerization_list

    def get_containerization(self):
        return self.containerization

    def set_dbms(self, dbms_list):
        self.dbms = dbms_list

    def get_dbms(self):
        return self.dbms

    def set_BaaS_platform(self, BaaS_platform_list):
        self.BaaS_platform = BaaS_platform_list

    def get_BaaS_platform(self):
        return self.BaaS_platform

    def set_cloud_platform(self, cloud_platform_list):
        self.cloud_platform = cloud_platform_list

    def get_cloud_platform(self):
        return self.cloud_platform

    def set_others(self, others_list):
        self.others = others_list

    def get_others(self):
        return self.others

class Projects(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(60), nullable=False)
    description = Column(String(150), nullable=False)
    link = Column(String(150), nullable=False)

class Contact(Base):
    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    phone = Column(String(30), nullable=False)
    x = Column(String(60), nullable=True)
    github = Column(String(60), nullable=True)
    linkedin = Column(String(60), nullable=True)
    website = Column(String(60), nullable=True)