# app/accounts/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import repository, model
from typing import cast # <--- IMPORTAR O CAST

# --- SERVIÇOS DE LEITURA (READ) ---

def get_all_accounts_for_user(db: Session, id_user: int):
    """Retorna todas as contas do usuário logado."""
    return repository.get_accounts_by_user(db, id_user=id_user)

def get_account_by_id(db: Session, id_account: int, id_user: int):
    """Busca uma conta específica, verificando se ela pertence ao usuário logado."""
    db_account = repository.get_account(db, id_account=id_account)
    if db_account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
    # VERIFICAÇÃO DE PERMISSÃO
    # CORREÇÃO DEFINITIVA: Usamos 'cast(int, ...)' para dizer ao Pylance:
    # "Confie em mim, 'db_account.usuario_id' é um 'int' neste ponto."
    if cast(int, db_account.usuario_id) != id_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this account")
        
    return db_account

# --- SERVIÇO DE CRIAÇÃO (CREATE) ---

def create_new_account(db: Session, account: model.AccountCreate, id_user: int):
    """Cria uma nova conta para o usuário logado."""
    # (Opcional) Adicionar lógicas de negócio, ex: limite de contas por usuário
    return repository.create_account(db=db, account=account, id_user=id_user)

# --- SERVIÇO DE ATUALIZAÇÃO (UPDATE) ---

def update_existing_account(db: Session, id_account: int, account_in: model.AccountUpdate, id_user: int):
    """Atualiza uma conta, verificando a permissão."""
    db_account = get_account_by_id(db, id_account=id_account, id_user=id_user) # Reusa a lógica de validação
    return repository.update_account(db=db, db_account=db_account, account_in=account_in)

# --- SERVIÇO DE DELEÇÃO (DELETE) ---

def delete_account_by_id(db: Session, id_account: int, id_user: int):
    """Deleta uma conta, verificando a permissão."""
    db_account = get_account_by_id(db, id_account=id_account, id_user=id_user) # Reusa a lógica de validação
    # (Opcional) Adicionar lógicas, ex: não deletar se saldo != 0
    return repository.delete_account(db=db, db_account=db_account)