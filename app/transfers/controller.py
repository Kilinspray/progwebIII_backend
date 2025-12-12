# app/transfers/controller.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, cast # <-- Importa o 'cast' para corrigir o Pylance

from database import get_db
from . import service, model # Irá importar o service (próximo passo)
# Importa o 'get_current_user' para proteger as rotas
from app.auth.service import get_current_user, require_role
from app.users.model import UserPublic, User as SQLAlchemyUser # Importa o schema Pydantic 'UserPublic'

# Este é o NOVO controller, agora protegido e usando SQLAlchemy
router = APIRouter(prefix="/transfers", tags=["Transfers"])

@router.post("/", response_model=model.TransferPublic, status_code=status.HTTP_201_CREATED)
def create_transfer(
    transfer: model.TransferCreate, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Cria uma nova transferência entre contas do usuário logado.
    """
    # Passa o ID do usuário logado para o serviço (com 'cast' para Pylance)
    return service.create_new_transfer(db=db, transfer=transfer, id_user=cast(int, current_user.id))

@router.get("/", response_model=List[model.TransferPublic])
def list_transfers_for_current_user(
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Lista todas as transferências pertencentes ao usuário logado.
    """
    # Passa o ID do usuário logado para o serviço (com 'cast' para Pylance)
    return service.get_all_transfers_for_user(db=db, id_user=cast(int, current_user.id))

@router.get("/{transfer_id}", response_model=model.TransferPublic)
def get_transfer(
    transfer_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Busca uma transferência específica do usuário logado pelo ID.
    """
    return service.get_transfer_by_id(db=db, transfer_id=transfer_id, id_user=cast(int, current_user.id))

@router.delete("/{transfer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transfer(
    transfer_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Deleta uma transferência do usuário logado.
    Nota: Transferências geralmente não devem ser deletadas (apenas anuladas), mas permitimos por simplicidade.
    """
    service.delete_transfer_by_id(db=db, transfer_id=transfer_id, id_user=cast(int, current_user.id))
    return

# --- ENDPOINTS ADMIN ---

@router.get("/admin/all", response_model=List[model.TransferPublic])
def list_all_transfers_admin(
    db: Session = Depends(get_db),
    current_user: SQLAlchemyUser = Depends(require_role("admin"))
):
    """
    Lista todas as transferências de todos os usuários (apenas para admin).
    """
    return service.get_all_transfers_admin(db=db)