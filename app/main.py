from fastapi import FastAPI, Depends, status
from typing import List, Optional
from sqlmodel import SQLModel, Session

from app.database import engine, get_session
from app import models
from app.schemas import (
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate
)
from app.crud import (
    create_employee,
    get_employee_by_id,
    list_employees,
    update_employee,
    delete_employee
)

app = FastAPI(title="Employee Management API")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.post(
    "/api/employees/",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED
)
def create_emp(
    data: EmployeeCreate,
    session: Session = Depends(get_session)
):
    return create_employee(session, data)


@app.get(
    "/api/employees/",
    response_model=List[EmployeeRead]
)
def get_employees(
    page: int = 1,
    size: int = 10,
    department: Optional[str] = None,
    role: Optional[str] = None,
    session: Session = Depends(get_session)
):
    return list_employees(
        session,
        page=page,
        size=size,
        department=department,
        role=role
    )

@app.get(
    "/api/employees/{id}",
    response_model=EmployeeRead
)
def get_employee(
    id: int,
    session: Session = Depends(get_session)
):
    return get_employee_by_id(session, id)


@app.put(
    "/api/employees/{id}",
    response_model=EmployeeRead
)
def update_emp(
    id: int,
    data: EmployeeUpdate,
    session: Session = Depends(get_session)
):
    return update_employee(session, id, data)


@app.delete(
    "/api/employees/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_emp(
    id: int,
    session: Session = Depends(get_session)
):
    delete_employee(session, id)
