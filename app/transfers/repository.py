# app/transfers/repository.py
from sqlalchemy.orm import Session
from . import model # Importa o model.py de 'transfers'

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---

def create_transfer(db: Session, transfer: model.TransferCreate, user_id: int):
    """
    Cria uma nova transferência no banco de dados.
    """
    # Cria o objeto do SQLAlchemy
    db_transfer = model.Transfer(
        valor=transfer.valor,
        data=transfer.data,
        conta_origem_id=transfer.conta_origem_id,
        conta_destino_id=transfer.conta_destino_id,
        usuario_id=user_id # Associa ao usuário logado
    )
    
    db.add(db_transfer)
    db.commit()
    db.refresh(db_transfer)
    return db_transfer

# --- FUNÇÕES DE LEITURA (READ) ---

def get_transfer(db: Session, transfer_id: int):
    """Busca uma transferência pelo ID."""
    return db.query(model.Transfer).filter(model.Transfer.id == transfer_id).first()

def get_transfers_by_user(db: Session, user_id: int):
    """
    Busca todas as transferências de um usuário específico, ordenadas pela mais recente.
    """
    return db.query(model.Transfer).filter(
        model.Transfer.usuario_id == user_id
    ).order_by(model.Transfer.data.desc()).all()

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---

def delete_transfer(db: Session, db_transfer: model.Transfer):
    """Deleta uma transferência do banco de dados."""
    db.delete(db_transfer)
    db.commit()
    return db_transfer

def get_all_transfers(db: Session):
    """Retorna todas as transferências de todos os usuários (para admin)."""
    return db.query(model.Transfer).order_by(model.Transfer.data.desc()).all()