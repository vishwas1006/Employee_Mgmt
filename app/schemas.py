from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel
from pydantic import EmailStr, field_validator

class EmployeeCreate(SQLModel):
    name: str
    email: EmailStr
    department: Optional[str] = None
    role: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name must not be empty")
        return v

class EmployeeRead(SQLModel):
    id: int
    name: str
    email: EmailStr
    department: Optional[str]
    role: Optional[str]
    date_joined: datetime

class EmployeeUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    role: Optional[str] = None
