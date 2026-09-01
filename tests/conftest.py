#   Esse arquivo é onde coloca as fixtures para
# deixar os codigos de teste mais limpo, sem
# precisar importar para os outros test já
# que é uma configuração propria do pytest

from contextlib import contextmanager
from datetime import datetime

import pytest

# Importando o cliente de test
from fastapi.testclient import TestClient

# Imposta o motor que se conectar com o DB
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

# Imortando o recurso que vai ser testado
from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import User, table_registry


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
@pytest.fixture
def session():
    # Cria a conexao com o banco de dados em memoria
    # Aqui é o connect do psycopg2
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # pega os metadados criados em tabela_registry e cria na engine
    # O (engine) é o db que as tabelas vao ficar
    table_registry.metadata.create_all(engine)

    # Abrir uma seção de troca entre o db e codigo
    # aqui seria a criação da sessao para fazer os executs do psycopg2
    with Session(engine) as session:
        # yield "pausa" a função e manda o dado para a função que chamou
        yield session

    # Deleta todas as tabelas do tabela_registry do engine - db
    table_registry.metadata.drop_all(engine)


# TUDO ISSO PARA CRIAR UM TEMPO FALSOOOOOOOO


@pytest.fixture
def created_user(session: Session):

    user = User(username='bob', email='bob@gmail.com', password='senha123')
    session.add(user)
    session.commit()
    session.refresh(user)

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
