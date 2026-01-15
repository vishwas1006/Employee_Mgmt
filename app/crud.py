from typing import Optional, List
from sqlmodel import Session, select
from fastapi import HTTPException, status

from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate


def create_employee(session: Session, data: EmployeeCreate) -> Employee:
    # check duplicate email
    statement = select(Employee).where(Employee.email == data.email)
    existing = session.exec(statement).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    employee = Employee.from_orm(data)
    session.add(employee)
    session.commit()
    session.refresh(employee)

    return employee


def get_employee_by_id(session: Session, employee_id: int) -> Employee:
    employee = session.get(Employee, employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    return employee


def list_employees(
    session: Session,
    page: int = 1,
    size: int = 10,
    department: Optional[str] = None,
    role: Optional[str] = None,
) -> List[Employee]:

    statement = select(Employee)

    if department:
        statement = statement.where(Employee.department == department)

    if role:
        statement = statement.where(Employee.role == role)

    offset = (page - 1) * size
    statement = statement.offset(offset).limit(size)

    return session.exec(statement).all()


def update_employee(
    session: Session,
    employee_id: int,
    data: EmployeeUpdate
) -> Employee:

    employee = session.get(Employee, employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(employee, key, value)

    session.add(employee)
    session.commit()
    session.refresh(employee)

    return employee


def delete_employee(session: Session, employee_id: int) -> None:
    employee = session.get(Employee, employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    session.delete(employee)
    session.commit()
