from http import HTTPStatus

# Framework FastApi
from fastapi import FastAPI

from fastapi_zero.schemas import Mensagem

from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get(
    '/', # No caminho /
    status_code=HTTPStatus.OK, 
    response_model=Mensagem  # schema (model) | o modelo pre definido que tem que ser enviado
)  
def read_root():
    return {'message': 'Olá mundo!'}

@app.get(
    '/teste', # endpoint | caminho
    status_code=HTTPStatus.OK, 
    response_class= HTMLResponse
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
