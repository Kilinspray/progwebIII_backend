# security.py
import os
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from pydantic import BaseModel

# --- CONFIGURAÇÕES DE SEGURANÇA ---
# Chave secreta para assinar os tokens JWT.
# Em produção, defina a variável de ambiente SECRET_KEY no Render
SECRET_KEY = os.getenv("SECRET_KEY", "8f3a1b2c4d5e6f70")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Tempo de validade do token

# --- HASHING DE SENHA (ARGON2ID) ---
# Argon2id é o algoritmo de hashing recomendado pela OWASP (2024)
# Mais seguro que bcrypt contra ataques GPU/ASIC modernos
# ALTERADO: schemes=["bcrypt"] -> schemes=["argon2"] para resolver incompatibilidade
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se uma senha em texto puro corresponde a um hash salvo."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha em texto puro usando Argon2id."""
    return pwd_context.hash(password)

# --- GERENCIAMENTO DE TOKEN JWT ---

def create_access_token(data: dict):
    """Cria um novo token de acesso JWT."""
    to_encode = data.copy()
    # Define o tempo de expiração com fuso horário (timezone-aware)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Schema Pydantic para os dados que guardamos dentro do token
class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None