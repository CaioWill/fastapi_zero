from http import HTTPStatus


def test_get_token(client, created_user):
    response = client.post(
        '/auth/token',
        data={
            'username': created_user.email,
            'password': created_user.clean_password,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'
