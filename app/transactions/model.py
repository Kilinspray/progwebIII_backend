# app/transactions/model.py
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict
from database import Base
from datetime import date
# Importa o Enum de Categoria para reuso (Despesa/Receita)
from app.categories.model import CategoryType 

# 2. Modelo da Tabela (SQLAlchemy)
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(500))
    # Usamos Numeric para dinheiro
    valor = Column(Numeric(15, 2), nullable=False)
    tipo = Column(Enum(CategoryType), nullable=False) # Reusa o Enum 'Despesa'/'Receita'
    data = Column(Date, nullable=False, default=date.today)
    
    # Chaves Estrangeiras
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    conta_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    # Uma transação pode não ter categoria (ex: transferência interna)
    categoria_id = Column(Integer, ForeignKey("categories.id"), nullable=True) 
    
    # Relacionamentos (para o SQLAlchemy 'entender' as ligações)
    owner = relationship("User")
    account = relationship("Account")
    category = relationship("Category")

# 3. Schemas (Pydantic)
# Schema base com campos comuns
class TransactionBase(BaseModel):
    descricao: str | None = Field(default=None, max_length=500)
    valor: float = Field(gt=0) # Valor deve ser sempre positivo
    tipo: CategoryType
    data: date
    conta_id: int
    categoria_id: int | None = None

# Schema para criar uma transação
class TransactionCreate(TransactionBase):
    pass

# Schema para atualizar uma transação (não se pode mudar o tipo ou valor)
class TransactionUpdate(BaseModel):
    descricao: str | None = Field(default=None, max_length=500)
    data: date | None = None
    conta_id: int | None = None
    categoria_id: int | None = None

# Schema público (o que a API retorna)
class TransactionPublic(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    usuario_id: int