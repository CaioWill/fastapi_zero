#  Esse arquivo é onde coloca as fixtures para
# deixar os codigos de teste mais limpo, sem
# precisar importar para os outros test já
# que é uma configuração propria do pytest

import pytest

# Importando o cliente de test
from fastapi.testclient import TestClient

# Imortando o recurso que vai ser testado
from fastapi_zero.app import app


# Fixture é um bloco reutilizavel, é tipo herança em class
@pytest.fixture
def client():
    # Arranjo - criou o cliente
    return TestClient(app)
