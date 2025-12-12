# app/auth/controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from . import service as auth_service # Renomeado
from security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint de login. Recebe 'username' (que é o email) e 'password'
    em um formulário (form-data).
    """
    # O 'username' do OAuth2PasswordRequestForm é o nosso 'email'
    user = auth_service.authenticate_user(db, email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # O 'sub' (subject) é o email, e guardamos o 'role' no token
    token_data = {"sub": user.email, "role": user.role.name}
    access_token = create_access_token(data=token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}