from http import HTTPStatus

# Framework FastApi
from fastapi import (
    FastAPI,
    HTTPException,  # Biblioteca de erros, seria o Exception do python cru
)
from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import (
    Mensagem,
    UserDB,
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
    '/front',  # endpoint | caminho
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
def create_user(user: UserSchema):
    user_with_id = UserDB(
        **user.model_dump(),  # transfoma o modelo em um dicionario de volta
        id=len(datebase) + 1,
    )

    datebase.append(user_with_id)

    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    # Como o modelo é um dict, temos re retonar em dict
    return {'users': datebase}


@app.put(
    '/users/{user_id}',  # adicionamos a variavel, paramentro da url
    status_code=HTTPStatus.OK,
    response_model=UserPlublic,
)
# HTTP://localhost:8000/users/1 -> 1 é a variavel que definimos o paramentro
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(
        **user.model_dump(),  # transfoma o modelo em dicionario de volta
        id=user_id,
    )

    if user_id < 1 or user_id > len(datebase):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Não encontrei'
        )

    # o local do usuario na lista
    datebase[user_id - 1] = user_with_id
    return user_with_id
