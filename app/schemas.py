from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel

class EmployeeCreate(SQLModel):
    name: str
    email: str
    department: Optional[str] = None
    role: Optional[str] = None

class EmployeeRead(SQLModel):
    id: int
    name: str
    email: str
    department: Optional[str]
    role: Optional[str]
    date_joined: datetime


class EmployeeUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    role: Optional[str] = None
