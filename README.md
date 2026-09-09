# Gerenciador de Tarefas — API (FastAPI do Zero)

Projeto desenvolvido acompanhando o curso:
[FastAPI do Zero](https://fastapidozero.dunossauro.com/) (Dunossauro)  
[aulas em vídeo](https://www.youtube.com/playlist?list=PLOQgLBuj2-3KT9ZWvPmaGFQ0KjIez0403)  
[conteúdo complementar](https://www.youtube.com/playlist?list=PLR2rHG9gyzbI)  

API REST completa para gerenciamento de tarefas e usuários, construída com FastAPI, com autenticação, persistência de dados, testes automatizados, containerização e pipeline de integração contínua.

## Funcionalidades

- CRUD de usuários
- CRUD de tarefas
- Autenticação e autorização com JWT
- Persistência de dados com SQLAlchemy ORM e PostgreSQL
- Migrações de banco de dados com Alembic
- Testes automatizados com Pytest (cobertura de código monitorada)
- Containerização com Docker e Docker Compose
- Integração contínua (CI) com GitHub Actions — testes rodam automaticamente a cada push
- Deploy realizado com sucesso no Fly.io (atualmente fora do ar, para evitar custos de manutenção contínua)

## Tecnologias

Python, FastAPI, Pydantic, SQLAlchemy, Alembic, Pytest, PostgreSQL, Docker, GitHub Actions

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

## Como rodar com Docker

```bash
docker compose up -d
```

## Como rodar os testes

```bash
poetry test
```

---

Parte da minha trilha de estudos para desenvolvimento backend com Python.