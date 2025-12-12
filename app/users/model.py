# app/users/model.py
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from database import Base
import enum
# Importa o schema Pydantic de Role
from app.roles.model import RolePublic

# 1. Enum para moedas
class CurrencyType(str, enum.Enum):
    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CNY = "CNY"
    CAD = "CAD"
    AUD = "AUD"
    CHF = "CHF"
    INR = "INR"

# ==================================
# MODELO DA TABELA (SQLAlchemy)
# (Combina Informações_Úteis.txt + Encontro 5)
# ==================================
class User(Base):
    __tablename__ = "users"
    
    # --- Campos do Informações_Úteis.txt ---
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False) # -> "senha_hash"
    nome = Column(String(100), index=True, nullable=True) 
    moeda = Column(Enum(CurrencyType), nullable=False, default=CurrencyType.BRL)
    
    # --- Campos adicionados pelo Encontro 5 ---
    profile_image_base64 = Column(Text, nullable=True)  # Armazena imagem em base64
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False) # Chave estrangeira
    
    # Relacionamento com a tabela Role
    # lazy="joined" faz com que o 'role' seja carregado junto com o 'user'
    role = relationship("Role", lazy="joined") 

# ==================================
# SCHEMAS (Pydantic)
# (Refletem a estrutura acima para entrada e saída da API)
# ==================================
class UserCreate(BaseModel):
    """Schema para criar um usuário (o que o cliente envia)"""
    email: EmailStr
    password: str = Field(min_length=8)
    nome: str | None = Field(default=None, min_length=3, max_length=100)
    moeda: CurrencyType = Field(default=CurrencyType.BRL)
    profile_image_base64: str | None = None
    role_id: int = Field(description="ID do role (ex: 1 para admin, 2 para user)")

class UserUpdate(BaseModel):
    """Schema para atualizar um usuário (apenas campos permitidos)"""
    nome: str | None = Field(default=None, max_length=100)
    moeda: CurrencyType | None = Field(default=None)
    profile_image_base64: str | None = None

class UserPublic(BaseModel):
    """Schema para retornar dados públicos do usuário (o que a API envia)"""
    model_config = ConfigDict(from_attributes=True) # Habilita modo ORM

    id: int
    email: EmailStr
    nome: str | None
    moeda: CurrencyType
    profile_image_base64: str | None
    role: RolePublic # Retorna o objeto Role aninhado