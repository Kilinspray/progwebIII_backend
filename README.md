# Projeto Final - API de Gestão Financeira

API REST desenvolvida com FastAPI para gestão de usuários, contas, transações e transferências.

## 🚀 Tecnologias

- **Python 3.13**
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL** - Banco de dados relacional
- **Pydantic** - Validação de dados
- **Passlib & Argon2** - Criptografia de senhas
- **Python-JOSE** - Autenticação JWT
- **Docker & Docker Compose** - Containerização

## 📋 Pré-requisitos

- Python 3.13+
- Poetry (gerenciador de dependências)
- PostgreSQL 16+ (ou Docker)
- Docker e Docker Compose (opcional)

## 🔧 Instalação

### Opção 1: Com Docker (Recomendado)

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd backend
```

2. Execute com Docker Compose:
```bash
docker-compose up -d
```

3. A API estará disponível em `http://localhost:8000`
4. Documentação interativa em `http://localhost:8000/docs`

### Opção 2: Instalação Local

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd backend
```

2. Instale as dependências com Poetry:
```bash
poetry install
```

3. Configure o banco de dados PostgreSQL e atualize a string de conexão em `database.py`:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://usuario:senha@localhost:5432/web3"
```

4. Ative o ambiente virtual:
```bash
poetry shell
```

5. Execute a aplicação:
```bash
uvicorn app.main:app --reload
```

## 🗂️ Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── accounts/            # Módulo de contas
│   ├── auth/                # Autenticação e autorização
│   ├── categories/          # Categorias de transações
│   ├── roles/               # Roles de usuários
│   ├── transactions/        # Transações financeiras
│   ├── transfers/           # Transferências entre contas
│   └── users/               # Gestão de usuários
├── database.py              # Configuração do banco de dados
├── security.py              # Funções de segurança
├── pyproject.toml           # Dependências do projeto
├── Dockerfile               # Imagem Docker
└── docker-compose.yml       # Orquestração de containers
```

## 📚 Documentação da API

Após iniciar a aplicação, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Autenticação

A API utiliza JWT (JSON Web Tokens) para autenticação. 

### Roles Padrão:
- **Admin** (id: 1) - Acesso administrativo completo
- **User** (id: 2) - Usuário comum

## 🐳 Comandos Docker Úteis

```bash
# Iniciar containers
docker-compose up -d

# Parar containers
docker-compose down

# Ver logs
docker-compose logs -f

# Reconstruir imagens
docker-compose up -d --build

# Acessar o container
docker-compose exec web bash

# Parar e remover volumes (CUIDADO: apaga dados do banco)
docker-compose down -v
```

## 🛠️ Desenvolvimento

### Executar em modo de desenvolvimento:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Executar testes:
```bash
poetry run pytest
```

## 📝 Variáveis de Ambiente

Crie um arquivo `.env` baseado em `.env.example`:

```env
DATABASE_URL=postgresql://postgres:senha@localhost:5432/web3
SECRET_KEY=sua-chave-secreta-aqui
```

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 👤 Autor

**Pedro Pereira Silva**
- Email: pedro10jti@gmail.com

---

⌨️ com ❤️ por [Pedro Pereira Silva](https://github.com/seu-usuario)
