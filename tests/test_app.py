# todo arquivo de teste tem que comecar com test_
from http import HTTPStatus

from fastapi_zero.schemas import UserPlublic


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


def test_creat_user_conflited(client, created_user):
    # conflict in username
    response = client.post(
        '/users/',
        json={'username': 'bob', 'email': 'test@test.com', 'password': 'test'},
    )

    # conflict in email
    response2 = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': 'bob@gmail.com',
            'password': 'test',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response2.status_code == HTTPStatus.CONFLICT


# Test para conferir o modelo de resposta do get users
def test_read_users(client, created_user, token):
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    user_schema = UserPlublic.model_validate(created_user).model_dump()

    assert response.status_code == HTTPStatus.OK
    # ele sempre dropa o banco, ai ele retorna vazio
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, created_user, token):
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': '123',
        },
    )
    response2 = client.put(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': '123',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }

    assert response2.status_code == HTTPStatus.UNAUTHORIZED


# Erro de integridade, ver se os uniques estão funcionando
def test_update_integrity_erro(client, created_user, token):
    # Post do novo user
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@gmail.com',
            'password': 'senha123',
        },
    )

    # Campo com unique igual
    res_update = client.put(
        f'/users/{created_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'fausto@gmail.com',
            'password': 'test',
        },
    )

    assert res_update.status_code == HTTPStatus.CONFLICT
    assert res_update.json() == {'detail': 'User name or Email already exists'}


def test_get_user_id(client, created_user):

    response = client.get('/users/1')

    response2 = client.get('/users/2')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@gmail.com',
        'id': 1,
    }

    assert response2.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, created_user, token):

    response = client.delete(
        f'/users/{created_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    response2 = client.delete('/users/2')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Delete'}

    assert response2.status_code == HTTPStatus.UNAUTHORIZED


def test_get_token(client, created_user):
    response = client.post(
        '/token',
        data={
            'username': created_user.email,
            'password': created_user.clean_password,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'
