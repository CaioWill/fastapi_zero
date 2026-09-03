from dataclasses import asdict

import pytest
from sqlalchemy import select

from fastapi_zero.models import User


@pytest.mark.asyncio
async def test_user_db(session, mock_db_time):
    # chamando a função de alteração do created_at
    with mock_db_time(model=User) as time:
        user_new = User(username='bob', email='bob@test', password='secret')

        session.add(user_new)  # insert user_new na sessao
        await session.commit()  # Commitando no db

        # o scarlars convert tudo do banco em objeto python de forma escalar
        # aqui e tipo o fatchall
        user = await session.scalar(select(User).where(User.username == 'bob'))

    # asdict transforma o resultado do select em um dicionario
    assert asdict(user) == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@test',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }
