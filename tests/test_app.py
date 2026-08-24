# todo arquivo de teste tem que comecar com test_

from http import HTTPStatus

# Importando o cliente de test
from fastapi.testclient import TestClient

# Imortando o arquivo que vai ser testado
from fastapi_zero.app import app


# aqui ele esta criando um cliente para fazer o test do app
def test_root_deve_retornar_ola_mundo():
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - arranjo
    - A: Act     - Executa a coisa (o SUT) 
    - A: Assert  - Garanta que A == A
    """
    # Arranjo - oque precia antes, oque precisa para fazer
    client = TestClient(app)

    # ACT - A coisa que esta sendo testada
    response = client.get('/')

    # assert - garanta que.
    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK
