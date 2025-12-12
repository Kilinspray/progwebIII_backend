# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal

# 1. Importa todos os seus controllers
from .users import controller as users_controller
from .roles import controller as roles_controller 
from .auth import controller as auth_controller 
from .accounts import controller as accounts_controller
from .categories import controller as categories_controller
from .transactions import controller as transactions_controller
from .transfers import controller as transfers_controller

# Importa modelos para criação de roles padrão
from .roles.model import Role

# 2. Cria todas as tabelas (definidas em models.py) que herdam de 'Base'
Base.metadata.create_all(bind=engine)

# 3. Cria roles padrão se não existirem
def create_default_roles():
    db = SessionLocal()
    try:
        # Verifica se já existem roles
        existing_roles = db.query(Role).count()
        if existing_roles == 0:
            # Cria roles padrão
            admin_role = Role(id=1, name="admin", description="Administrador do sistema")
            user_role = Role(id=2, name="user", description="Usuário comum")
            db.add(admin_role)
            db.add(user_role)
            db.commit()
            print("✅ Roles padrão criados: admin (1) e user (2)")
    except Exception as e:
        print(f"⚠️ Erro ao criar roles padrão: {e}")
        db.rollback()
    finally:
        db.close()

create_default_roles()

app = FastAPI(title="API do Meu Projeto", version="0.1.0")

# CORS - permite requisições do Flutter Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],  # Permite todos os headers
)

# 3. Inclui os roteadores de cada módulo na aplicação principal
app.include_router(users_controller.router)
app.include_router(roles_controller.router) 
app.include_router(auth_controller.router)
app.include_router(accounts_controller.router)
app.include_router(categories_controller.router)
app.include_router(transactions_controller.router)
app.include_router(transfers_controller.router)

@app.get("/")
def read_root():
    return {"message": "API está no ar!"}