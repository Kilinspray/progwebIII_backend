# app/auth/service.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import ValidationError
from jose import JWTError, jwt
from database import get_db
from app.users import repository as user_repository # Corrigido
from security import verify_password, SECRET_KEY, ALGORITHM, TokenData
from app.users.model import User # Corrigido

# Define o "esquema" de autenticação.
# 'tokenUrl' é o endpoint que o cliente usará para obter o token (o /auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def authenticate_user(db: Session, email: str, password: str):
    """
PCA-5.4: Use of Code Generation Tools
I have generated the following code using a large language model.
    Verifica se um usuário existe e se a senha está correta.
    """
    user = user_repository.get_user_by_email(db, email=email)
    # CORREÇÃO 2: Cast para str() para ajudar o Pylance a entender o tipo
    if not user or not verify_password(password, str(user.hashed_password)):
        return None
    # Retorna o objeto User completo se a autenticação for bem-sucedida
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependência que decodifica o token e retorna o usuário atual.
    Usado para proteger endpoints.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # CORREÇÃO 1: payload.get() pode retornar None
        email: str | None = payload.get("sub")
        role: str | None = payload.get("role")
        if email is None or role is None:
            raise credentials_exception
        token_data = TokenData(email=email, role=role)
    except (JWTError, ValidationError):
        raise credentials_exception

    # CORREÇÃO 3: Usar a variável 'email' (que já sabemos que não é None)
    # em vez de 'token_data.email' (que ainda é 'str | None')
    user = user_repository.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

def require_role(required_role_name: str):
    """
    Factory de dependência que verifica se o usuário atual tem o perfil (role) necessário.
    """
    def role_checker(current_user: User = Depends(get_current_user)):
        # Verifica se o usuário tem um 'role' e se o nome do 'role' é o exigido
        if not current_user.role or current_user.role.name != required_role_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for this user role"
            )
        return current_user
    return role_checker