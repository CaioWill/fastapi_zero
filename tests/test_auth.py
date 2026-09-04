from http import HTTPStatus

from freezegun import freeze_time


def test_token_wrong_email_and_password(client, created_user):
    response1 = client.post(
        '/auth/token',
        data={
            'username': created_user.username,
            'password': created_user.clean_password,
        },
    )
    response2 = client.post(
        '/auth/token',
        data={
            'username': created_user.email,
            'password': '123',
        },
    )
    assert response1.status_code == HTTPStatus.UNAUTHORIZED
    assert response1.json() == {'detail': 'Incorrect email or password'}

    assert response2.status_code == HTTPStatus.UNAUTHORIZED
    assert response2.json() == {'detail': 'Incorrect email or password'}


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


def test_get_refresh_token(client, created_user, token):
    response = client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert data['token_type'] == 'Bearer'


def test_token_expired_after_time(client, created_user):

    with freeze_time('2026-04-09 14:30:00'):
        response = client.post(
            '/auth/token',
            data={
                'username': created_user.email,
                'password': created_user.clean_password,
            },
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']
    with freeze_time('2026-04-09 15:01:00'):
        response = client.put(
            f'/users/{created_user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'fausto',
                'email': 'fausto@gmail.com',
                'password': 'test',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_token_expired_dont_refresh(client, created_user):
    with freeze_time('2026-04-09 14:30:00'):
        response = client.post(
            '/auth/token',
            data={
                'username': created_user.email,
                'password': created_user.clean_password,
            },
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2026-04-09 15:01:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Cloud not validate credentials'}
