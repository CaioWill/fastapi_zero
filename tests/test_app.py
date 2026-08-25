# todo arquivo de teste tem que comecar com test_
from http import HTTPStatus


# aqui ele esta criando um cliente para fazer o test do app
def test_root_deve_retornar_ola_mundo(client):
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - arranjo
    - A: Act     - Executa a coisa o SUT
    - A: Assert  - Garanta que A == A
    """
    # ACT - fez uma requisição get via cliente no caminho /
    response = client.get('/')

    # assert - garanta que. - viu se retorna 200 OK e se a mensagem é ola mundo
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo!'}


# Test para saber se o post user esta funcionando corretamente
def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': 'bob@examplo.com',
            'password': '1234',
        },  # Criando o Json enviado pro post para fazer o test
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@examplo.com',
    }


# Test para conferir o modelo de resposta do get users
def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'username': 'bob', 'email': 'bob@examplo.com'}]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': '123',
        },
    )

    assert response.status_code == HTTPStatus(HTTPStatus.OK)
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }
