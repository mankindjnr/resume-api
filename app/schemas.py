from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from pydantic.types import conint

# ====================  Summary  ====================
class SummaryBase(BaseModel):
    summary: str

    class Config:
        orm_mode = True

class Summary(SummaryBase):
    pass