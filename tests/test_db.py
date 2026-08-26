from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_user_db(session, mock_db_time):
    with mock_db_time(model=User) as time:
        user_new = User(username='test', email='test@test', password='secret')

        session.add(user_new)  # adicionando o user no db
        session.commit()  # Commitando no db

        # o scarlars convert tudo do banco em objeto python de forma escalar
        # aqui e tipo o fatchall
        user = session.scalar(select(User).where(User.username == 'test'))

    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test',
        'password': 'secret',
        'created_at': time,
    }
