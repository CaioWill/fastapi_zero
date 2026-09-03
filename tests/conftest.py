#   Esse arquivo é onde coloca as fixtures para
# deixar os codigos de teste mais limpo, sem
# precisar importar para os outros test já
# que é uma configuração propria do pytest

from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio

# Importando o cliente de test
from fastapi.testclient import TestClient

# Imposta o motor que se conectar com o DB
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

# Imortando o recurso que vai ser testado
from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import User, table_registry
from fastapi_zero.security import get_password_hash
from fastapi_zero.settings import Settings


# Fixture é um bloco reutilizavel, é tipo herança em class
@pytest.fixture
def client(session):
    # Arranjo - criou o cliente

    # A dependecia tem que ser uma função
    def get_session_override():
        return session

    # Sobre-escreve a dependecia em endpoints
    # altera o get_session para a função de cima
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    # desfaz o override da dependencia para o anterior
    app.dependency_overrides.clear()

    #   Isso é necessario para a sessão que for usada para os test
    # Ser a do db em memoria, o sqlite, criada na func a baixo


# Essa fixture abre uma sessão do db para os testes
# ele envia os dados de test e os apaga sozinho


# abre uma fixture async
@pytest_asyncio.fixture
async def session():
    # Cria a conexao com o banco de dados em memoria
    # Aqui é o connect do psycopg2
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # pega os metadados criados em tabela_registry e cria na engine
    # O (engine) é o db que as tabelas vao ficar
    async with engine.begin() as conn:
        # como as tabelas não podem ser criadas de forma asincrona
        # usamos o run_sync para rodar de foram sincrona
        await conn.run_sync(table_registry.metadata.create_all)

    # Abrir uma seção de troca entre o db e codigo
    # aqui seria a criação da sessao para fazer os executs do psycopg2
    async with AsyncSession(engine, expire_on_commit=False) as session:
        # yield "pausa" a função e manda o dado para a função que chamou
        yield session

    # Deleta todas as tabelas do tabela_registry do engine - db
    async with engine.begin() as conn:
        # da mesma forma de criar tambem e para apagar
        await conn.run_sync(table_registry.metadata.drop_all)


# TUDO ISSO PARA CRIAR UM TEMPO FALSOOOOOOOO


@pytest_asyncio.fixture
async def created_user(session: AsyncSession):
    password = 'senha123'
    user = User(
        username='bob',
        email='bob@gmail.com',
        password=get_password_hash(password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    # gambiarra, para conseguir a senha para fazer a verificação
    # não pessiste no banco
    user.clean_password = password

    return user


# Rodando em contexto - with
# função para
@contextmanager
def _mock_db_time(*, model, time=datetime(2026, 8, 21)):

    # um gacho para fazer alterações
    # tem que ter os tres parametros mesmo sem usar para o event funcionar
    def fake_time_hook(mapper, connection, target):
        # (Connection) é a conexão
        # (Target) é o objeto

        # hasattr verifica se objeto que veio tem o atributo antes de replace
        if hasattr(target, 'created_at'):
            target.created_at = time

        if hasattr(target, 'updated_at'):
            target.updated_at = time

    # é tipo o trigger do postgre no python
    event.listen(model, 'before_insert', fake_time_hook)

    # Pausa a função e manda o time para a função que chamou
    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def token(client, created_user):
    response = client.post(
        '/auth/token',
        data={
            'username': created_user.email,
            'password': created_user.clean_password,
        },
    )

    return response.json()['access_token']


@pytest.fixture
def settings():
    return Settings()
