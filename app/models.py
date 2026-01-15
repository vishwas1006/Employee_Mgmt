from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)

    department: Optional[str] = None
    role: Optional[str] = None

    date_joined: datetime = Field(default_factory=datetime.utcnow)
