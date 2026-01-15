from typing import Optional, List
from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate

def create_employee(session: Session, data: EmployeeCreate) -> Employee:
    existing = session.exec(
        select(Employee).where(Employee.email == data.email)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    employee = Employee.model_validate(data)
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

def get_employee_by_id(session: Session, employee_id: int) -> Employee:
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

def list_employees(
    session: Session,
    page: int = 1,
    size: int = 10,
    department: Optional[str] = None,
    role: Optional[str] = None
) -> List[Employee]:

    stmt = select(Employee)

    if department:
        stmt = stmt.where(Employee.department == department)
    if role:
        stmt = stmt.where(Employee.role == role)

    stmt = stmt.offset((page - 1) * size).limit(size)
    return session.exec(stmt).all()

def update_employee(
    session: Session,
    employee_id: int,
    data: EmployeeUpdate
) -> Employee:

    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)

    session.commit()
    session.refresh(employee)
    return employee

def delete_employee(session: Session, employee_id: int):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    session.delete(employee)
    session.commit()
