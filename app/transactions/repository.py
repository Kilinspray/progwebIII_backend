# app/transactions/repository.py
from sqlalchemy.orm import Session
from . import model
from datetime import date

# --- FUNÇÕES DE LEITURA (READ) ---

def get_transaction(db: Session, transaction_id: int):
    """Busca uma transação pelo ID."""
    return db.query(model.Transaction).filter(model.Transaction.id == transaction_id).first()

def get_transactions_by_user(db: Session, user_id: int):
    """Busca todas as transações de um usuário específico, ordenadas pela mais recente."""
    return db.query(model.Transaction).filter(
        model.Transaction.usuario_id == user_id
    ).order_by(model.Transaction.data.desc()).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---

def create_transaction(db: Session, transaction: model.TransactionCreate, user_id: int):
    """Cria uma nova transação no banco de dados."""
    
    # Cria o objeto do SQLAlchemy
    db_transaction = model.Transaction(
        descricao=transaction.descricao,
        valor=transaction.valor,
        tipo=transaction.tipo,
        data=transaction.data,
        conta_id=transaction.conta_id,
        categoria_id=transaction.categoria_id,
        usuario_id=user_id # Associa ao usuário logado
    )
    
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---

def update_transaction(db: Session, db_transaction: model.Transaction, transaction_in: model.TransactionUpdate):
    """Atualiza os dados de uma transação."""
    # Converte o schema Pydantic para um dicionário, excluindo campos não enviados
    update_data = transaction_in.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
         setattr(db_transaction, key, value)
         
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---

def delete_transaction(db: Session, db_transaction: model.Transaction):
    """Deleta uma transação do banco de dados."""
    db.delete(db_transaction)
    db.commit()
    return db_transaction