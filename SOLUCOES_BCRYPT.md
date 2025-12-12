# 🔐 Soluções para Problema bcrypt + Passlib

## 📊 Problema Identificado

**Ambiente:**
- Python: 3.13.7
- bcrypt: 5.0.0
- passlib: 1.7.4

**Erro:** Incompatibilidade entre Passlib 1.7.4 (2020) e bcrypt 5.0.0 (2024)

---

## ✅ SOLUÇÃO 1: Atualizar Passlib (RECOMENDADA)

### Por que usar:
- Mantém código atual
- Passlib tem versões mais recentes no GitHub
- Compatível com bcrypt 5.x

### Comandos:
```powershell
# Opção A: Usar fork mantido (bcrypt-passlib)
poetry remove passlib
poetry add bcrypt-passlib

# OU Opção B: Instalar direto do GitHub
poetry remove passlib
poetry add git+https://github.com/pyca/bcrypt-passlib.git
```

### Alteração no código:
**NENHUMA** - código continua igual

### Prós:
✅ Sem mudança de código
✅ Mantém Passlib (amplamente testado)
✅ Suporte a múltiplos algoritmos

### Contras:
⚠️ Depende de fork/versão não oficial

---

## ✅ SOLUÇÃO 2: Downgrade bcrypt

### Por que usar:
- Mantém código 100% igual
- bcrypt 3.2.2 é estável e compatível

### Comandos:
```powershell
poetry remove bcrypt
poetry add "bcrypt==3.2.2"
```

### Alteração no código:
**NENHUMA**

### Prós:
✅ Zero mudanças
✅ Versão estável e testada
✅ Compatibilidade garantida

### Contras:
⚠️ Usa versão antiga do bcrypt
⚠️ Pode ter vulnerabilidades corrigidas em versões novas

---

## ✅ SOLUÇÃO 3: Trocar para Argon2id (MAIS SEGURA)

### Por que usar:
- **Argon2id é o algoritmo de hashing de senha recomendado em 2024/2025**
- Vencedor do Password Hashing Competition (2015)
- Resistente a ataques GPU/ASIC
- Mais seguro que bcrypt contra ataques modernos

### Comandos:
```powershell
poetry add argon2-cffi
# passlib continua instalado para compatibilidade futura
```

### Alterações no código:

**1. `security.py`:**
```python
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from pydantic import BaseModel

# --- CONFIGURAÇÕES DE SEGURANÇA ---
SECRET_KEY = "sua-chave-secreta-super-dificil-deve-ser-trocada"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- HASHING DE SENHA (ARGON2) ---
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se uma senha em texto puro corresponde a um hash salvo."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha em texto puro usando Argon2."""
    return pwd_context.hash(password)

# ... resto do código igual
```

**Apenas troca:** `schemes=["bcrypt"]` → `schemes=["argon2"]`

### Prós:
✅ **Mais seguro** (padrão OWASP 2024)
✅ Resistente a ataques GPU/ASIC
✅ Configurável (memória, tempo, paralelismo)
✅ Funciona perfeitamente no Windows

### Contras:
⚠️ Precisa migrar hashes existentes (se houver usuários)
⚠️ Ligeiramente mais lento (mas isso é bom para segurança)

---

## ✅ SOLUÇÃO 4: Usar bcrypt Nativo (Sem Passlib)

### Por que usar:
- Menos dependências
- bcrypt 5.x funciona perfeitamente sozinho
- Controle total sobre hashing

### Comandos:
```powershell
# bcrypt já está instalado (5.0.0)
# Passlib pode ser removido:
poetry remove passlib
```

### Alterações no código:

**1. `security.py`:**
```python
import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from pydantic import BaseModel

# --- CONFIGURAÇÕES DE SEGURANÇA ---
SECRET_KEY = "sua-chave-secreta-super-dificil-deve-ser-trocada"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- HASHING DE SENHA (BCRYPT NATIVO) ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se uma senha em texto puro corresponde a um hash salvo."""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
    )

def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha em texto puro usando bcrypt."""
    salt = bcrypt.gensalt(rounds=12)  # 12 rounds = bom equilíbrio
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # Retorna string para salvar no DB

# ... resto do código (JWT) igual
```

### Prós:
✅ Usa bcrypt 5.x (mais recente)
✅ Menos dependências
✅ Código simples e direto

### Contras:
⚠️ Perde flexibilidade do Passlib (trocar algoritmo facilmente)
⚠️ Precisa migrar código existente

---

## 🎯 RECOMENDAÇÃO FINAL

**Para desenvolvimento/aprendizado:** SOLUÇÃO 2 (downgrade)
- Zero mudanças, funciona imediatamente

**Para produção/projeto real:** SOLUÇÃO 3 (Argon2)
- Mais seguro, padrão moderno, 1 linha de mudança

---

## 📝 Passos para Implementar

Escolha UMA solução e execute os comandos. Vou implementar a Solução 3 (Argon2) por padrão se você aprovar.
