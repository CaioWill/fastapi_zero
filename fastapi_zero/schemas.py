from pydantic import BaseModel, EmailStr


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


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    #  Esse modelo diz que vai retonar um dic com dados em uma
    # list e esses dados tem o modelo UserPublic
    users: list[UserPlublic]
