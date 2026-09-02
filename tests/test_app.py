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
