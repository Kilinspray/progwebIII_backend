# app/categories/controller.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, cast # <-- Importa o 'cast' para corrigir o Pylance

from database import get_db
from . import service, model
# Importa o 'get_current_user' para proteger as rotas
from app.auth.service import get_current_user
from app.users.model import UserPublic # Importa o schema Pydantic 'UserPublic'

# Este é o NOVO controller, agora protegido e usando SQLAlchemy
router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=model.CategoryPublic, status_code=status.HTTP_201_CREATED)
def create_category(
    category: model.CategoryCreate, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Cria uma nova categoria para o usuário logado.
    """
    # Usa 'cast' para corrigir o erro do Pylance
    return service.create_new_category(db=db, category=category, user_id=cast(int, current_user.id))

@router.get("/", response_model=List[model.CategoryPublic])
def list_categories_for_current_user(
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Lista todas as categorias pertencentes ao usuário logado.
    """
    # Usa 'cast' para corrigir o erro do Pylance
    return service.get_all_categories_for_user(db=db, user_id=cast(int, current_user.id))

@router.get("/{category_id}", response_model=model.CategoryPublic)
def get_category(
    category_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Busca uma categoria específica do usuário logado pelo ID.
    """
    # Usa 'cast' para corrigir o erro do Pylance
    return service.get_category_by_id(db=db, category_id=category_id, user_id=cast(int, current_user.id))

@router.put("/{category_id}", response_model=model.CategoryPublic)
def update_category(
    category_id: int, 
    category_in: model.CategoryUpdate, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Atualiza uma categoria do usuário logado.
    """
    # Usa 'cast' para corrigir o erro do Pylance
    return service.update_existing_category(db=db, category_id=category_id, category_in=category_in, user_id=cast(int, current_user.id))

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Deleta uma categoria do usuário logado.
    """
    # Usa 'cast' para corrigir o erro do Pylance
    service.delete_category_by_id(db=db, category_id=category_id, user_id=cast(int, current_user.id))
    # Resposta 204 não deve ter corpo
    return