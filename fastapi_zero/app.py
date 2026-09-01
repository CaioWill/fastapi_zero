from http import HTTPStatus

# Framework FastApi
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,  # Biblioteca de erros, seria o Exception do python cru
)
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Mensagem,
    UserList,
    UserPlublic,
    UserSchema,
)

app = FastAPI()

datebase = []


@app.get(
    '/',  # No caminho /
    status_code=HTTPStatus.OK,
    # schema (model) | o modelo pre definido que vai retornar pro cliente
    response_model=Mensagem,
)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get(
    '/front/',  # endpoint | caminho
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse,  # Tipo do dado enviado
)
def read_root_teste():
    return """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""


@app.post(
    '/users/',  # endpoint, pedaço da url que representa esse pedaço de codigo
    status_code=HTTPStatus.CREATED,  # Retorna 201 - Created
    response_model=UserPlublic,  # Schema de resposta
)
# oque vinher no parametro user é convertido no objeto UserSchema
def create_user(
    user: UserSchema,
    session: Session = Depends(get_session),
    # com Depends, sempre que chama ela e exec
):

    # session = get_session() -> dessa for so seria executado a func uma vez

    response = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if response:
        if response.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif response.email == user.email:
            raise HTTPException(
                HTTPStatus.CONFLICT, detail='Email already exixts'
            )

    response = User(**user.model_dump())
    session.add(response)
    session.commit()
    session.refresh(response)

    return response


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 9, offset: int = 0, session: Session = Depends(get_session)
):

    users = session.scalars(select(User).limit(limit).offset(offset))

    # Como o modelo é um dict, temos re retonar em dict
    return {'users': users}


@app.put(
    '/users/{user_id}',  # adicionamos a variavel, paramentro da url
    status_code=HTTPStatus.OK,
    response_model=UserPlublic,
)
# HTTP://localhost:8000/users/1 -> 1 é a variavel que definimos o paramentro
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    try:
        user_db.email = user.email
        user_db.username = user.username
        user_db.password = user.password

        session.add(user_db)
        session.commit()

        return user_db

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User name or Email already exists',
        )


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPlublic
)
def get_user_id(user_id: int, session: Session = Depends(get_session)):

    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return user_db


@app.delete(
    '/users/{user_id}',  # adicionamos a variavel, paramentro da url
    status_code=HTTPStatus.OK,
    response_model=Mensagem,
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(user_db)
    session.commit()

    return {'message': 'User Delete'}
