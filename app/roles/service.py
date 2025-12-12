# app/roles/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import repository, model

def create_new_role(db: Session, role: model.RoleCreate):
    db_role = repository.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role name already exists")
    return repository.create_role(db=db, role=role)

def get_all(db: Session):
    return repository.get_all_roles(db)