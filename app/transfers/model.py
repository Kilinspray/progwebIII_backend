# app/transfers/model.py
from sqlalchemy import Column, Integer, ForeignKey, Numeric, Date, CheckConstraint
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict, field_validator
from database import Base
from datetime import date

# 1. Modelo da Tabela (SQLAlchemy)
class Transfer(Base):
    __tablename__ = "transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    # Usamos Numeric para dinheiro, conforme boa prática (seu TXT pede 'float')
    valor = Column(Numeric(15, 2), nullable=False)
    data = Column(Date, nullable=False, default=date.today)
    
    # Chaves Estrangeiras (conforme seu TXT)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    conta_origem_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    conta_destino_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    
    # Relacionamentos (para o SQLAlchemy funcionar)
    owner = relationship("User")
    account_from = relationship("Account", foreign_keys=[conta_origem_id])
    account_to = relationship("Account", foreign_keys=[conta_destino_id])
    
    # Regra de negócio (baseada no seu script SQL)
    __table_args__ = (
        CheckConstraint("conta_origem_id <> conta_destino_id", name="chk_conta_origem_destino_diferentes"),
    )

# 2. Schemas (Pydantic) - O que a API usa
class TransferBase(BaseModel):
    """Schema base para Transferência."""
    valor: float = Field(gt=0) # Valor deve ser positivo
    data: date
    conta_origem_id: int | None = Field(default=None, description="Se não informado, usa a primeira conta do usuário")
    conta_destino_id: int

    # Validação Pydantic para garantir que os IDs são diferentes
    @field_validator('conta_destino_id')
    def contas_diferentes(cls, v, info):
        if 'conta_origem_id' in info.data and info.data['conta_origem_id'] is not None and v == info.data['conta_origem_id']:
            raise ValueError("Conta de origem e destino não podem ser a mesma")
        return v

class TransferCreate(TransferBase):
    """Schema para CRIAR uma transferência."""
    pass

# Transferências geralmente não são atualizáveis, então não há schema Update.

class TransferPublic(TransferBase):
    """Schema PÚBLICO (o que a API retorna)."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    usuario_id: int