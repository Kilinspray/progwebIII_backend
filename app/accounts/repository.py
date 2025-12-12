# app/accounts/repository.py
from sqlalchemy.orm import Session
from . import model

# --- FUNÇÕES DE LEITURA (READ) ---

def get_account(db: Session, id_account: int):
    """Busca uma conta pelo ID."""
    return db.query(model.Account).filter(model.Account.id == id_account).first()

def get_accounts_by_user(db: Session, id_user: int):
    """Busca todas as contas de um usuário específico."""
    return db.query(model.Account).filter(model.Account.usuario_id == id_user).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---

def create_account(db: Session, account: model.AccountCreate, id_user: int):
    """Cria uma nova conta no banco de dados."""
    # O saldo atual começa igual ao saldo inicial
    db_account = model.Account(
        nome=account.nome,
        tipo=account.tipo,
        saldo_inicial=account.saldo_inicial,
        saldo_atual=account.saldo_inicial, # Saldo atual = Saldo inicial
        limite_credito=account.limite_credito,
        usuario_id=id_user # Associa ao usuário logado
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---

def update_account(db: Session, db_account: model.Account, account_in: model.AccountUpdate):
    """Atualiza os dados de uma conta (nome ou limite)."""
    update_data = account_in.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
         setattr(db_account, key, value)
         
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---

def delete_account(db: Session, db_account: model.Account):
    """Deleta uma conta do banco de dados."""
    db.delete(db_account)
    db.commit()
    return db_account