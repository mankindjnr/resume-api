from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
import datetime

class Summary(Base):
    __tablename__ = 'summary'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    summary = Column(String(150), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
