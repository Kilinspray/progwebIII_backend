# app/categories/model.py
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict
from database import Base
import enum

# 1. Cria o Enum para os tipos de categoria (baseado no Informações_Úteis.txt)
class CategoryType(str, enum.Enum):
    DESPESA = "Despesa"
    RECEITA = "Receita"

# 2. Modelo da Tabela (SQLAlchemy)
class Category(Base):
    """
    Representa a tabela 'categories' no banco de dados.
    """
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(Enum(CategoryType), nullable=False)
    
    # Chave Estrangeira
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relacionamento (para o SQLAlchemy entender a ligação)
    owner = relationship("User")
    
    # Garante que um usuário não tenha categorias duplicadas (mesmo nome e tipo)
    # (baseado no Informações_Úteis.txt)
    __table_args__ = (UniqueConstraint("usuario_id", "nome", "tipo", name="_usuario_nome_tipo_uc"),)

# 3. Schemas (Pydantic) - O "contrato" da sua API

class CategoryBase(BaseModel):
    """Schema base para Categoria (campos comuns)."""
    nome: str = Field(min_length=3, max_length=100)
    tipo: CategoryType

class CategoryCreate(CategoryBase):
    """Schema usado para CRIAR uma categoria via API."""
    pass

class CategoryUpdate(BaseModel):
    """Schema usado para ATUALIZAR uma categoria via API."""
    nome: str | None = Field(default=None, min_length=3, max_length=100)
    tipo: CategoryType | None = None

class CategoryPublic(CategoryBase):
    """Schema usado para RETORNAR dados de uma categoria ao cliente."""
    model_config = ConfigDict(from_attributes=True) # Permite ler dados do modelo SQLAlchemy
    
    id: int
    usuario_id: int