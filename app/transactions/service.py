# app/transactions/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import cast
from decimal import Decimal

from . import repository, model
from app.accounts import repository as accounts_repository # Para validar a conta
from app.categories.model import CategoryType

def _update_account_balance_after_transaction(db: Session, account_id: int, valor: float, tipo: CategoryType, is_new: bool = True):
    """
    Atualiza o saldo da conta após uma transação.
    - Despesa: subtrai do saldo
    - Receita: adiciona ao saldo
    - is_new=True para nova transação, is_new=False para reverter (delete)
    """
    db_account = accounts_repository.get_account(db, id_account=account_id)
    if db_account:
        valor_decimal = Decimal(str(valor))
        saldo_atual = Decimal(str(db_account.saldo_atual))
        
        if is_new:
            if tipo == CategoryType.DESPESA:
                db_account.saldo_atual = float(saldo_atual - valor_decimal)
            else:  # RECEITA
                db_account.saldo_atual = float(saldo_atual + valor_decimal)
        else:
            # Reverter transação (ao deletar)
            if tipo == CategoryType.DESPESA:
                db_account.saldo_atual = float(saldo_atual + valor_decimal)
            else:  # RECEITA
                db_account.saldo_atual = float(saldo_atual - valor_decimal)
        db.commit()
        db.refresh(db_account)

# --- SERVIÇO DE CRIAÇÃO (CREATE) ---
def create_new_transaction(db: Session, transaction: model.TransactionCreate, user_id: int):
    """Cria uma nova transação, validando se a conta pertence ao usuário."""
    # Valida se a conta informada pertence ao usuário
    db_account = accounts_repository.get_account(db, id_account=transaction.conta_id)
    if not db_account or cast(int, db_account.usuario_id) != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found or does not belong to the user")
    
    # Cria a transação
    db_transaction = repository.create_transaction(db=db, transaction=transaction, user_id=user_id)
    
    # Atualiza o saldo da conta
    _update_account_balance_after_transaction(db, transaction.conta_id, transaction.valor, transaction.tipo, is_new=True)
    
    return db_transaction

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
    
    # Reverter o saldo antes de deletar
    _update_account_balance_after_transaction(
        db, 
        cast(int, db_transaction.conta_id), 
        cast(float, db_transaction.valor), 
        db_transaction.tipo, 
        is_new=False
    )
    
    return repository.delete_transaction(db=db, db_transaction=db_transaction)