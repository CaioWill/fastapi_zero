from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Valalida in|out put de dados conferindo se estão no padrão pre definido
# Schemas ou (models) | classe para definir a forma esperada de um dado
# Aqui seria tipo um check do Postgres, confere se o dado de message é uma str
class Mensagem(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    # EmailStr - Ele valida se é um email, uma str com @ ...
    email: EmailStr
    password: str


class UserPlublic(BaseModel):
    username: str
    email: EmailStr
    id: int
    # permite que o pydantic leia dados de um atributo de objeto comum
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    #  Esse modelo diz que vai retonar um dic com dados em uma
    # list e esses dados tem o modelo UserPublic
    users: list[UserPlublic]


# Schema do Token
class Token(BaseModel):
    access_token: str
    token_type: str


# Schema querry
class FilterPage(BaseModel):
    # coloca um valor minimo e um default
    limit: int = Field(ge=0, default=9)

    # o Field é para colocar um valor minimo e o default
    offset: int = Field(ge=0, default=0)
