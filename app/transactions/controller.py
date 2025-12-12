# app/transactions/controller.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, cast # <-- Importa o 'cast' para corrigir o Pylance

from database import get_db
from . import service, model
# Importa o 'get_current_user' para proteger as rotas
from app.auth.service import get_current_user
from app.users.model import UserPublic # Importa o schema Pydantic 'UserPublic'

# Este é o NOVO controller, agora protegido e usando SQLAlchemy
router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=model.TransactionPublic, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: model.TransactionCreate, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Cria uma nova transação (receita ou despesa) para o usuário logado.
    """
    # Passa o ID do usuário logado para o serviço (com 'cast' para Pylance)
    return service.create_new_transaction(db=db, transaction=transaction, user_id=cast(int, current_user.id))

@router.get("/", response_model=List[model.TransactionPublic])
def list_transactions_for_current_user(
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Lista todas as transações do usuário logado.
    """
    # Passa o ID do usuário logado para o serviço (com 'cast' para Pylance)
    return service.get_all_transactions_for_user(db=db, user_id=cast(int, current_user.id))

@router.get("/{transaction_id}", response_model=model.TransactionPublic)
def get_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Busca uma transação específica do usuário logado.
    """
    # Passa o ID do usuário para validação no serviço (com 'cast' para Pylance)
    return service.get_transaction_by_id(db=db, transaction_id=transaction_id, user_id=cast(int, current_user.id))

@router.put("/{transaction_id}", response_model=model.TransactionPublic)
def update_transaction(
    transaction_id: int, 
    transaction_in: model.TransactionUpdate, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Atualiza uma transação do usuário logado.
    """
    # Passa o ID do usuário para validação no serviço (com 'cast' para Pylance)
    return service.update_existing_transaction(
        db=db, 
        transaction_id=transaction_id, 
        transaction_in=transaction_in, 
        user_id=cast(int, current_user.id)
    )

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Deleta uma transação do usuário logado.
    """
    # Passa o ID do usuário para validação no serviço (com 'cast' para Pylance)
    service.delete_transaction_by_id(db=db, transaction_id=transaction_id, user_id=cast(int, current_user.id))
    # Resposta 204 não deve ter corpo
    return