# app/users/controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from .model import UserCreate, UserPublic, UserUpdate
from . import service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário.
    """
    return service.create_new_user(db=db, user=user)

@router.get("/", response_model=List[UserPublic])
def list_users(db: Session = Depends(get_db)):
    """
    Lista todos os usuários.
    """
    return service.get_all_users(db=db)

@router.put("/{id_user}", response_model=UserPublic)
def update_user(id_user: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Atualiza um usuário existente.
    """
    return service.update_existing_user(db=db, id_user=id_user, user_in=user_update)

@router.delete("/{id_user}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id_user: int, db: Session = Depends(get_db)):
    """
    Deleta um usuário existente.
    """
    service.delete_user_by_id(db=db, id_user=id_user)
    return
