# app/transactions/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import cast

from . import repository, model
from app.accounts import repository as accounts_repository # Para validar a conta

# --- SERVIÇO DE CRIAÇÃO (CREATE) ---
def create_new_transaction(db: Session, transaction: model.TransactionCreate, user_id: int):
    """Cria uma nova transação, validando se a conta pertence ao usuário."""
    # Valida se a conta informada pertence ao usuário
    db_account = accounts_repository.get_account(db, id_account=transaction.conta_id)
    if not db_account or cast(int, db_account.usuario_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found or does not belong to the user")
    
    # (Opcional) Validar se a categoria pertence ao usuário
    # ...

    return repository.create_transaction(db=db, transaction=transaction, user_id=user_id)

# --- SERVIÇOS DE LEITURA (READ) ---
def get_all_transactions_for_user(db: Session, user_id: int):
    """Retorna todas as transações do usuário."""
    return repository.get_transactions_by_user(db, user_id=user_id)

def get_transaction_by_id(db: Session, transaction_id: int, user_id: int):
    """Busca uma transação, verificando se ela pertence ao usuário."""
    db_transaction = repository.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    
    if cast(int, db_transaction.usuario_id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this transaction")
        
    return db_transaction

# --- SERVIÇO DE ATUALIZAÇÃO (UPDATE) ---
def update_existing_transaction(db: Session, transaction_id: int, transaction_in: model.TransactionUpdate, user_id: int):
    """Atualiza uma transação, verificando a permissão."""
    # Reutiliza a lógica que verifica se a transação existe e pertence ao usuário
    db_transaction = get_transaction_by_id(db, transaction_id=transaction_id, user_id=user_id)
    
    # (Opcional) Adicionar validações extras se necessário
    # ...

    return repository.update_transaction(db=db, db_transaction=db_transaction, transaction_in=transaction_in)

# --- SERVIÇO DE DELEÇÃO (DELETE) ---
def delete_transaction_by_id(db: Session, transaction_id: int, user_id: int):
    """Deleta uma transação, verificando a permissão."""
    # Reutiliza a lógica que verifica se a transação existe e pertence ao usuário
    db_transaction = get_transaction_by_id(db, transaction_id=transaction_id, user_id=user_id)
    return repository.delete_transaction(db=db, db_transaction=db_transaction)