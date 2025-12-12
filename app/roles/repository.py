# app/roles/role_repository.py
from sqlalchemy.orm import Session
from . import model

def get_role_by_name(db: Session, name: str):
    return db.query(model.Role).filter(model.Role.name == name).first()

# --- ADICIONE ESTA FUNÇÃO ---
def get_role_by_id(db: Session, id: int):
    return db.query(model.Role).filter(model.Role.id == id).first()
# ------------------------------

# Funções básicas do CRUD para Roles
def get_all_roles(db: Session):
    return db.query(model.Role).all()

def create_role(db: Session, role: model.RoleCreate):
    db_role = model.Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role