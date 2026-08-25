from http import HTTPStatus

# Framework FastApi
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import Mensagem

app = FastAPI()


@app.get(
    '/',  # No caminho /
    status_code=HTTPStatus.OK,
    # schema (model) | o modelo pre definido que tem que ser enviado
    response_model=Mensagem,
)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get(
    '/teste',  # endpoint | caminho
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse,
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
