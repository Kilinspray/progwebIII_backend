# app/accounts/controller.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from . import service, model
# Importa o 'get_current_user' para proteger as rotas
from app.auth.service import get_current_user, require_role
# Importa o 'User' do SQLAlchemy e 'UserPublic' do Pydantic
from app.users.model import User as SQLAlchemyUser, UserPublic

# Este é o NOVO controller, agora protegido e usando SQLAlchemy
router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/", response_model=model.AccountPublic, status_code=status.HTTP_201_CREATED)
def create_account(
    account: model.AccountCreate, 
    db: Session = Depends(get_db), 
    # CORREÇÃO: Usar o 'UserPublic' como o tipo da dependência
    # O 'get_current_user' ainda retorna o modelo SQLAlchemy,
    # mas o FastAPI vai convertê-lo para 'UserPublic' para nós.
    current_user: UserPublic = Depends(get_current_user) # <- Proteção
):
    """
    Cria uma nova conta para o usuário logado.
    """
    # Passa o ID do usuário logado para o serviço
    # Agora 'current_user.id' é corretamente tipado como 'int'
    return service.create_new_account(db=db, account=account, id_user=current_user.id)

@router.get("/", response_model=List[model.AccountPublic])
def list_accounts_for_current_user(
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção e CORREÇÃO
):
    """
    Lista todas as contas pertencentes ao usuário logado.
    """
    # Agora 'current_user.id' é corretamente tipado como 'int'
    return service.get_all_accounts_for_user(db=db, id_user=current_user.id)

@router.get("/{id_account}", response_model=model.AccountPublic)
def get_account(
    id_account: int, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção e CORREÇÃO
):
    """
    Busca uma conta específica do usuário logado pelo ID.
    """
    # Agora 'current_user.id' é corretamente tipado como 'int'
    return service.get_account_by_id(db=db, id_account=id_account, id_user=current_user.id)

@router.put("/{id_account}", response_model=model.AccountPublic)
def update_account(
    id_account: int, 
    account_in: model.AccountUpdate, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção e CORREÇÃO
):
    """
    Atualiza uma conta do usuário logado (nome ou limite de crédito).
    """
    # Agora 'current_user.id' é corretamente tipado como 'int'
    return service.update_existing_account(db=db, id_account=id_account, account_in=account_in, id_user=current_user.id)

@router.delete("/{id_account}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    id_account: int, 
    db: Session = Depends(get_db), 
    current_user: UserPublic = Depends(get_current_user) # <- Proteção e CORREÇÃO
):
    """
    Deleta uma conta do usuário logado.
    """
    # Agora 'current_user.id' é corretamente tipado como 'int'
    service.delete_account_by_id(db=db, id_account=id_account, id_user=current_user.id)
    # Resposta 204 não deve ter corpo
    return

# --- ENDPOINTS ADMIN ---

@router.get("/admin/all", response_model=List[model.AccountPublic])
def list_all_accounts_admin(
    db: Session = Depends(get_db),
    current_user: SQLAlchemyUser = Depends(require_role("admin"))
):
    """
    Lista todas as contas de todos os usuários (apenas para admin).
    """
    return service.get_all_accounts_admin(db=db)