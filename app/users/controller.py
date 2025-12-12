# app/users/controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from database import get_db
from .model import UserCreate, UserPublic, UserUpdate
from . import service
from app.auth.service import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

# Schema para atualizar avatar
class AvatarUpdate(BaseModel):
    profile_image_base64: str

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

# IMPORTANTE: Rotas /me devem vir ANTES das rotas com {id_user}
@router.get("/me", response_model=UserPublic)
def get_current_user_info(current_user: UserPublic = Depends(get_current_user)):
    """
    Retorna os dados do usuário logado, incluindo foto de perfil.
    """
    return current_user

@router.put("/me/avatar", response_model=UserPublic)
def update_my_avatar(
    avatar: AvatarUpdate,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user)
):
    """
    Atualiza a foto de perfil do usuário logado.
    """
    user_update = UserUpdate(profile_image_base64=avatar.profile_image_base64)
    return service.update_existing_user(db=db, id_user=current_user.id, user_in=user_update)

@router.put("/me", response_model=UserPublic)
def update_my_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserPublic = Depends(get_current_user)
):
    """
    Atualiza os dados do perfil do usuário logado (nome, moeda, avatar).
    """
    return service.update_existing_user(db=db, id_user=current_user.id, user_in=user_update)

# Rotas com parâmetro {id_user} devem vir DEPOIS das rotas /me
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
