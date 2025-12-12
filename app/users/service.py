# app/users/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import repository, model # Importa repository.py e model.py
from app.roles import repository as roles_repository # Importa o repo de roles

def create_new_user(db: Session, user: model.UserCreate):
    db_user = repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Verifica se o 'role_id' enviado existe no banco
    db_role = roles_repository.get_role_by_id(db, id=user.role_id)
    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with ID {user.role_id} not found")

    return repository.create_user(db=db, user=user)

def get_all_users(db: Session):
    return repository.get_users(db)

def get_user_by_id(db: Session, id_user: int):
    db_user = repository.get_user(db, id_user=id_user)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

def update_existing_user(db: Session, id_user: int, user_in: model.UserUpdate):
    db_user = get_user_by_id(db, id_user)
    return repository.update_user(db=db, db_user=db_user, user_in=user_in)

def delete_user_by_id(db: Session, id_user: int):
    db_user = get_user_by_id(db, id_user)
    return repository.delete_user(db=db, db_user=db_user)