# app/transfers/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import cast # <-- Importa o 'cast' para corrigir o Pylance
from decimal import Decimal

from . import repository, model
# Importa o 'service' de contas para reusar a lógica de validação
from app.accounts import service as accounts_service
from app.accounts import repository as accounts_repository

# --- LÓGICA DE NEGÓCIO ---
def _update_account_balances_for_transfer(db: Session, conta_origem_id: int, conta_destino_id: int, valor: float, is_new: bool = True):
    """
    Atualiza os saldos das contas após uma transferência.
    - Conta origem: subtrai o valor
    - Conta destino: adiciona o valor
    - is_new=True para nova transferência, is_new=False para reverter (delete)
    """
    db_origem = accounts_repository.get_account(db, id_account=conta_origem_id)
    db_destino = accounts_repository.get_account(db, id_account=conta_destino_id)
    
    if db_origem and db_destino:
        valor_decimal = Decimal(str(valor))
        saldo_origem = Decimal(str(db_origem.saldo_atual))
        saldo_destino = Decimal(str(db_destino.saldo_atual))
        
        if is_new:
            db_origem.saldo_atual = float(saldo_origem - valor_decimal)
            db_destino.saldo_atual = float(saldo_destino + valor_decimal)
        else:
            # Reverter transferência (ao deletar)
            db_origem.saldo_atual = float(saldo_origem + valor_decimal)
            db_destino.saldo_atual = float(saldo_destino - valor_decimal)
        db.commit()
        db.refresh(db_origem)
        db.refresh(db_destino)

# --- SERVIÇO DE CRIAÇÃO (CREATE) ---

def create_new_transfer(db: Session, transfer: model.TransferCreate, id_user: int):
    """
    Cria uma nova transferência, validando ambas as contas e o saldo.
    """
    
    # 1. Se conta_origem_id não foi informado, usa a primeira conta do usuário
    conta_origem_id = transfer.conta_origem_id
    if conta_origem_id is None:
        # Tenta pegar a primeira conta do usuário
        first_account = accounts_service.get_all_accounts_for_user(db, id_user=id_user)
        if not first_account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não possui nenhuma conta. Crie uma conta antes de fazer transferências."
            )
        conta_origem_id = cast(int, first_account[0].id)
    
    # 2. Valida a Conta de Origem:
    db_account_origem = accounts_service.get_account_by_id(
        db, id_account=conta_origem_id, id_user=id_user
    )
    
    # 3. Valida a Conta de Destino:
    db_account_destino = accounts_service.get_account_by_id(
        db, id_account=transfer.conta_destino_id, id_user=id_user
    )
    
    # 4. Valida Saldo Suficiente:
    if cast(float, db_account_origem.saldo_atual) < transfer.valor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saldo insuficiente na conta de origem."
        )

    # 5. Cria o registro da transferência (com conta_origem_id preenchida)
    transfer_with_origem = model.TransferCreate(
        valor=transfer.valor,
        data=transfer.data,
        conta_origem_id=conta_origem_id,
        conta_destino_id=transfer.conta_destino_id
    )
    db_transfer = repository.create_transfer(db=db, transfer=transfer_with_origem, user_id=id_user)
    
    # 6. Atualiza os saldos das contas
    _update_account_balances_for_transfer(db, conta_origem_id, transfer.conta_destino_id, transfer.valor, is_new=True)
    
    return db_transfer

# --- SERVIÇOS DE LEITURA (READ) ---

def get_all_transfers_for_user(db: Session, id_user: int):
    """Retorna todas as transferências do usuário logado."""
    return repository.get_transfers_by_user(db, user_id=id_user)

def get_transfer_by_id(db: Session, transfer_id: int, id_user: int):
    """Busca uma transferência específica, verificando se ela pertence ao usuário logado."""
    db_transfer = repository.get_transfer(db, transfer_id=transfer_id)
    if db_transfer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transfer not found")
    
    if cast(int, db_transfer.usuario_id) != id_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this transfer")
        
    return db_transfer

# --- SERVIÇO DE DELEÇÃO (DELETE) ---

def delete_transfer_by_id(db: Session, transfer_id: int, id_user: int):
    """Deleta uma transferência, verificando a permissão."""
    db_transfer = get_transfer_by_id(db, transfer_id=transfer_id, id_user=id_user)
    
    # Reverter os saldos antes de deletar
    _update_account_balances_for_transfer(
        db,
        cast(int, db_transfer.conta_origem_id),
        cast(int, db_transfer.conta_destino_id),
        cast(float, db_transfer.valor),
        is_new=False
    )
    
    return repository.delete_transfer(db=db, db_transfer=db_transfer)

# --- SERVIÇOS ADMIN ---

def get_all_transfers_admin(db: Session):
    """Retorna todas as transferências de todos os usuários (apenas para admin)."""
    return repository.get_all_transfers(db)