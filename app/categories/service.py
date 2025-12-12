# app/categories/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import repository, model
from typing import cast # <-- Importa o 'cast' para corrigir o Pylance

# --- SERVIÇOS DE LEITURA (READ) ---

def get_all_categories_for_user(db: Session, user_id: int):
    """Retorna todas as categorias do usuário logado."""
    return repository.get_categories_by_user(db, user_id=user_id)

def get_category_by_id(db: Session, category_id: int, user_id: int):
    """Busca uma categoria específica, verificando se ela pertence ao usuário logado."""
    db_category = repository.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    # VERIFICAÇÃO DE PERMISSÃO (usando 'cast' para evitar erro do Pylance)
    if cast(int, db_category.usuario_id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this category")
        
    return db_category

# --- SERVIÇO DE CRIAÇÃO (CREATE) ---

def create_new_category(db: Session, category: model.CategoryCreate, user_id: int):
    """Cria uma nova categoria para o usuário logado."""
    # Verifica se já existe uma categoria com mesmo nome e tipo para este usuário
    db_existing_category = repository.get_category_by_name_and_type(
        db, user_id=user_id, name=category.nome, tipo=category.tipo
    )
    # CORREÇÃO: O Pylance se confunde com 'if db_existing_category:'
    # Esta verificação é mais robusta.
    if db_existing_category is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category with this name and type already exists for this user")
        
    return repository.create_category(db=db, category=category, user_id=user_id)

# --- SERVIÇO DE ATUALIZAÇÃO (UPDATE) ---

def update_existing_category(db: Session, category_id: int, category_in: model.CategoryUpdate, user_id: int):
    """Atualiza uma categoria, verificando a permissão."""
    db_category = get_category_by_id(db, category_id=category_id, user_id=user_id) # Reusa a lógica de validação
    
    # (Opcional) Se o nome ou tipo foi alterado, verificar duplicatas
    # CORREÇÃO: Usamos 'cast' para forçar o Pylance a entender os tipos
    new_name = category_in.nome if category_in.nome is not None else cast(str, db_category.nome)
    new_tipo = category_in.tipo if category_in.tipo is not None else cast(model.CategoryType, db_category.tipo)
    
    # Verifica se os campos (novos ou antigos) mudaram
    if new_name != db_category.nome or new_tipo != db_category.tipo:
        db_existing_category = repository.get_category_by_name_and_type(
            db, user_id=user_id, name=new_name, tipo=new_tipo
        )
        if db_existing_category and cast(int, db_existing_category.id) != category_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category with this name and type already exists")

    return repository.update_category(db=db, db_category=db_category, category_in=category_in)

# --- SERVIÇO DE DELEÇÃO (DELETE) ---

def delete_category_by_id(db: Session, category_id: int, user_id: int):
    """Deleta uma categoria, verificando a permissão."""
    # (Adicionar verificação se a categoria está em uso antes de deletar)
    db_category = get_category_by_id(db, category_id=category_id, user_id=user_id) # Reusa a lógica de validação
    return repository.delete_category(db=db, db_category=db_category)