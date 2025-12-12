# app/roles/role_controller.py
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from . import service, model
# A linha abaixo será descomentada no próximo passo (auth)
# from auth.auth_service import require_role 

router = APIRouter(prefix="/roles", tags=["Roles"])

# A proteção 'dependencies' será adicionada no próximo passo
@router.post("/", response_model=model.RolePublic, status_code=status.HTTP_201_CREATED)
             # dependencies=[Depends(require_role("admin"))])
def create_role(role: model.RoleCreate, db: Session = Depends(get_db)):
    """Cria um novo perfil (será protegido por 'admin' em breve)."""
    return service.create_new_role(db=db, role=role)

# A proteção 'dependencies' será adicionada no próximo passo
@router.get("/", response_model=List[model.RolePublic])
            # dependencies=[Depends(require_role("admin"))])
def list_roles(db: Session = Depends(get_db)):
    """Lista todos os perfis (será protegido por 'admin' em breve)."""
    return service.get_all(db)