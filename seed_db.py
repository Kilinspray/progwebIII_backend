# seed_db.py
"""
Script de seed para popular o banco de dados com dados iniciais.
Cria roles padrão e um usuário administrador.
Execute com: python seed_db.py
"""
from database import SessionLocal, Base, engine
from security import get_password_hash
from app.roles.model import Role
from app.users.model import User

def seed_database():
    """
    Popula o banco de dados com dados iniciais (roles e usuário admin).
    """
    
    # Garante que todas as tabelas foram criadas
    Base.metadata.create_all(bind=engine)
    
    # Cria uma sessão do banco
    db = SessionLocal()

    try:
        print("🌱 Iniciando seed do banco de dados...")

        # --- 1. Criar Roles (Perfis) ---
        admin_role = db.query(Role).filter(Role.name == 'admin').first()
        if not admin_role:
            admin_role = Role(id=1, name='admin', description='Administrador do sistema')
            db.add(admin_role)
            print("✅ Role 'admin' criada.")
        else:
            print("ℹ️  Role 'admin' já existe.")
        
        user_role = db.query(Role).filter(Role.name == 'user').first()
        if not user_role:
            user_role = Role(id=2, name='user', description='Usuário comum')
            db.add(user_role)
            print("✅ Role 'user' criada.")
        else:
            print("ℹ️  Role 'user' já existe.")
        
        # Commita as roles primeiro para que possamos usar os IDs
        db.commit()

        # --- 2. Criar Usuário Admin ---
        admin_email = 'admin@example.com'
        admin_user = db.query(User).filter(User.email == admin_email).first()
        
        if not admin_user:
            # A senha "admin123" só existe aqui, neste script.
            # Ela é hasheada antes de ser salva no banco de dados.
            admin_password = "admin123"
            hashed_password = get_password_hash(admin_password)

            admin_user = User(
                email=admin_email,
                hashed_password=hashed_password,
                full_name='Administrador do Sistema',
                role_id=admin_role.id,  # Associa com a role 'admin'
                preferred_currency='BRL'
            )
            db.add(admin_user)
            db.commit()
            print(f"✅ Usuário '{admin_email}' criado com sucesso.")
            print(f"   📧 Email: {admin_email}")
            print(f"   🔑 Senha: {admin_password}")
        else:
            print(f"ℹ️  Usuário '{admin_email}' já existe.")
        
        print("\n🎉 Seed do banco de dados concluído com sucesso!\n")

    except Exception as e:
        print(f"❌ Erro durante o seed: {e}")
        db.rollback()  # Desfaz qualquer mudança se um erro ocorrer
        raise
    finally:
        db.close()  # Fecha a sessão

if __name__ == "__main__":
    seed_database()
