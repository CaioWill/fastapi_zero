# Framework FastApi
from fastapi import FastAPI

app = FastAPI()


# Envolucro do /
@app.get('/')
def read_root():
    return {'message': 'Olá mundo!'}
