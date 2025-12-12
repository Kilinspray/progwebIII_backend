# app/accounts/model.py
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict
from database import Base
import enum

# 1. Cria o Enum para os tipos de conta (baseado no Informações_Úteis.txt)
class AccountType(str, enum.Enum):
    CARTEIRA = "Carteira"
    BANCO = "Banco"
    COFRE = "Cofre"
    INVESTIMENTO = "Investimento"
    OUTROS = "Outros"

# 2. Modelo da Tabela (SQLAlchemy)
class Account(Base):
    """
    Representa a tabela 'accounts' no banco de dados.
    """
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(Enum(AccountType), nullable=False)
    
    # Usamos Numeric(15, 2) para dinheiro. É o tipo correto, nunca use Float no DB.
    saldo_inicial = Column(Numeric(15, 2), nullable=False, default=0.00)
    saldo_atual = Column(Numeric(15, 2), nullable=False, default=0.00)
    limite_credito = Column(Numeric(15, 2), nullable=True, default=0.00)
    
    # Chave Estrangeira
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relacionamento (para o SQLAlchemy entender a ligação)
    owner = relationship("User")

# 3. Schemas (Pydantic) - O "contrato" da sua API

class AccountBase(BaseModel):
    """Schema base para Conta (campos comuns)."""
    nome: str = Field(min_length=3, max_length=100)
    tipo: AccountType
    # Pydantic pode usar float para validação de API, SQLAlchemy cuidará da conversão
    saldo_inicial: float = Field(default=0.0, ge=0) 
    limite_credito: float | None = Field(default=None, ge=0)

class AccountCreate(AccountBase):
    """Schema usado para CRIAR uma conta via API."""
    # O usuario_id virá do 'current_user' (usuário logado),
    # então não precisamos pedi-lo aqui.
    
    @classmethod
    def model_validate(cls, obj):
        """Validação customizada: limite_credito só para tipo Banco."""
        instance = super().model_validate(obj)
        if instance.limite_credito is not None and instance.limite_credito > 0:
            if instance.tipo != AccountType.BANCO:
                raise ValueError("limite_credito só pode ser definido para contas do tipo Banco")
        return instance

class AccountUpdate(BaseModel):
    """Schema usado para ATUALIZAR uma conta via API."""
    # Apenas alguns campos podem ser atualizados.
    # Saldo é atualizado via transações, não diretamente.
    nome: str | None = Field(default=None, min_length=3, max_length=100)
    limite_credito: float | None = Field(default=None, ge=0)
    tipo: AccountType | None = None  # Necessário para validação
    
    @classmethod
    def model_validate(cls, obj):
        """Validação customizada: limite_credito só para tipo Banco."""
        instance = super().model_validate(obj)
        if instance.limite_credito is not None and instance.limite_credito > 0:
            if instance.tipo is not None and instance.tipo != AccountType.BANCO:
                raise ValueError("limite_credito só pode ser definido para contas do tipo Banco")
        return instance

class AccountPublic(AccountBase):
    """Schema usado para RETORNAR dados de uma conta ao cliente."""
    model_config = ConfigDict(from_attributes=True) # Permite ler dados do modelo SQLAlchemy
    
    id: int
    usuario_id: int
    saldo_atual: float # Retorna o saldo atual