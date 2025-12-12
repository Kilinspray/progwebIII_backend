from database import SessionLocal
from app.users.model import User
from security import get_password_hash
import traceback

print("Starting test...")

db = SessionLocal()
try:
    hashed = get_password_hash('12345678')
    print('Hash:', hashed[:30])
    user = User(email='test5@test.com', hashed_password=hashed, nome='Test', moeda='BRL', role_id=1)
    print('User object created')
    db.add(user)
    print('User added to session')
    db.commit()
    print('Committed')
    db.refresh(user)
    print('User ID:', user.id)
except Exception as e:
    print('ERROR occurred:')
    traceback.print_exc()
finally:
    db.close()
    print('Done')
