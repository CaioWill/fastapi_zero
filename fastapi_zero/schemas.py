from pydantic import BaseModel


# Valalida a entrada e saida de dados conferindo se estão no padrão pre definido
# Schemas ou (models) | classe para definir a forma esperada de um dado
# Aqui seria tipo um check do Postgres, conferindo se o dado de message é uma str
class Mensagem(BaseModel):
    message: str
