# Framework FastApi
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapi_zero.routers import auth, users
from fastapi_zero.schemas import Mensagem

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)


# endpoint inicial
@app.get(
    '/',  # No caminho /
    status_code=HTTPStatus.OK,
    # schema (model) | o modelo pre definido que vai retornar pro cliente
    response_model=Mensagem,
)
def read_root():
    return {'message': 'Olá mundo!'}


# endpoint com html
@app.get(
    '/front/',  # endpoint | caminho
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse,  # Tipo do dado enviado
)
def read_root_teste():  # pragma: no cover
    return """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""
