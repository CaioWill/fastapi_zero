# Gerenciador de Tarefas — API (FastAPI do Zero)

> 🚧 Projeto em desenvolvimento — acompanhando o curso [FastAPI do Zero](https://fastapidozero.dunossauro.com/) (Dunossauro).

API REST para gerenciamento de tarefas e usuários, construída com FastAPI.

## Funcionalidades atuais

- CRUD de usuários
- CRUD de tarefas
- Autenticação e autorização com JWT
- Persistência de dados com SQLAlchemy ORM (SQLite no momento — migração para PostgreSQL prevista mais adiante no curso)
- Migrações de banco de dados com Alembic
- Estrutura de projeto refatorada (aula 7)

## Tecnologias

Python, FastAPI, Pydantic, SQLAlchemy, Alembic, Pytest

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
DATABASE_URL=          # conexão com o banco de dados
SECRET_KEY=             # chave usada para assinar/verificar o JWT
ALGORITHM=               # algoritmo de assinatura do JWT (ex: HS256)
ACCESS_TOKEN_EXPIRE_MINUTES=   # tempo de validade do token de acesso, em minutos
```

## Como rodar

```bash
poetry install
poetry shell
poetry server
```

---

Parte da minha trilha de estudos para desenvolvimento backend com Python.