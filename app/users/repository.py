# app/users/repository.py
from sqlalchemy.orm import Session
from . import model # Importa model.py
# A importação 'security' vai falhar até criarmos o 'auth'.
from security import get_password_hash 

# --- FUNÇÕES DE LEITURA (READ) ---
def get_user(db: Session, id_user: int):
    return db.query(model.User).filter(model.User.id == id_user).first()

def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()

def get_users(db: Session):
    return db.query(model.User).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---
def create_user(db: Session, user: model.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = model.User(
        email=user.email, 
        hashed_password=hashed_password, 
        nome=user.nome,
        moeda=user.moeda,
        profile_image_base64=user.profile_image_base64,
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---
def update_user(db: Session, db_user: model.User, user_in: model.UserUpdate):
    update_data = user_in.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
         setattr(db_user, key, value)
         
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---
def delete_user(db: Session, db_user: model.User):
    db.delete(db_user)
    db.commit()
    return db_user