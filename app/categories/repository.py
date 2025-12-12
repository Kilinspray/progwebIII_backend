# app/categories/repository.py
from sqlalchemy.orm import Session
from . import model

# --- FUNÇÕES DE LEITURA (READ) ---

def get_category(db: Session, category_id: int):
    """Busca uma categoria pelo ID."""
    return db.query(model.Category).filter(model.Category.id == category_id).first()

def get_category_by_name_and_type(db: Session, user_id: int, name: str, tipo: model.CategoryType):
    """Busca uma categoria pelo nome e tipo para um usuário (evitar duplicatas)."""
    return db.query(model.Category).filter(
        model.Category.usuario_id == user_id,
        model.Category.nome == name,
        model.Category.tipo == tipo
    ).first()

def get_categories_by_user(db: Session, user_id: int):
    """Busca todas as categorias de um usuário específico."""
    return db.query(model.Category).filter(model.Category.usuario_id == user_id).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---

def create_category(db: Session, category: model.CategoryCreate, user_id: int):
    """Cria uma nova categoria no banco de dados."""
    db_category = model.Category(
        nome=category.nome,
        tipo=category.tipo,
        usuario_id=user_id # Associa ao usuário logado
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---

def update_category(db: Session, db_category: model.Category, category_in: model.CategoryUpdate):
    """Atualiza os dados de uma categoria."""
    update_data = category_in.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
         setattr(db_category, key, value)
         
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---

def delete_category(db: Session, db_category: model.Category):
    """Deleta uma categoria do banco de dados."""
    db.delete(db_category)
    db.commit()
    return db_category