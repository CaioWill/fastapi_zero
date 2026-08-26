#  Esse arquivo é onde coloca as fixtures para
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

# Imortando o recurso que vai ser testado
from fastapi_zero.app import app
from fastapi_zero.models import table_registry


# Fixture é um bloco reutilizavel, é tipo herança em class
@pytest.fixture
def client():
    # Arranjo - criou o cliente
    return TestClient(app)


@pytest.fixture
def session():
    # Cria a conexao com o banco de dados em memoria
    # Aqui é o connect do psycopg2
    engine = create_engine('sqlite:///:memory:')

    # Pega os metadados dos 'modelos-class-tabelas' e as crias no engine
    # O (engine) é o db que as tabelas vao ficar
    table_registry.metadata.create_all(engine)

    # Abrir uma seção de troca entre o db e codigo
    # aqui seria a criação da sessao para fazer os executs do psycopg2
    with Session(engine) as session:
        # yield ele inicia a sessao e fica em processo ate acabar
        yield session

    # Deleta todas as tabelas
    table_registry.metadata.drop_all(engine)


# TUDO ISSO PARA CRIAR UM TEMPO FALSOOOOOOOO


# Rodando em contexto
@contextmanager
def _mock_db_time(*, model, time=datetime(2026, 8, 21)):
    def fake_time_hook(mapper, connection, target):
        # hasattr o objeto que veio tem o atributo
        if hasattr(target, 'created_at'):
            target.created_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
