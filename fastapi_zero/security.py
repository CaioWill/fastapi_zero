from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.settings import Settings

# Checa se veio na url um bearer token
# Se não tiver direciona para a url definida
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

# Descite por defull o melhor tipo de hash
pwd_context = PasswordHash.recommended()

settings = Settings()


# Faz a criptografia da senha em hash
def get_password_hash(password: str):
    return pwd_context.hash(password)


# comparação de hash
def verify_password(plain_password: str, hashed_password: str):
    # primeiro a senha limpa depois a com hash
    return pwd_context.verify(plain_password, hashed_password)


# Criação do JWT -> token de acesso
def create_access_token(data: dict):
    # Copia o dict que vem com a claims sub : email para a variavel
    to_encode = data.copy()

    # Cria a claims exp -> Horario de expiração do token
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )  # em minutos

    # Adiciona ao dict com o sub, tendo o payload com o sub e exp
    to_encode.update({'exp': expire})

    # Faz a criação do JWT (Token) ->
    # passa o payload, senha(segurança) e o algoritimo
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    # Retornar o Token
    return encoded_jwt


# Função para verificar sem tem um token válido
async def get_current_user(
    session: AsyncSession = Depends(get_session),
    # Chama a variavel para checar se veio um token
    token: str = Depends(oauth2_scheme),
):
    # Constant de erro
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Cloud not validate credentials',
        headers={'WWW-Autheticate': 'Bearer'},
    )

    # Faz a descodificação do Token usando a senha e o algoritimo
    try:
        # Descodando o TOKEN jwt
        playload = decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )

        # Pega o email do playload
        subject_email = playload.get('sub')

        # Confere se o email veio no sub:
        if not subject_email:
            raise credentials_exception

    # Caso o exp tenha expirado
    except DecodeError:
        raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    # Confere se o email esta no banco de dados
    user = await session.scalar(
        select(User).where(User.email == subject_email)
    )

    # Se o email nao estiver no banco de dados
    if not user:
        raise credentials_exception

    # retorna usuario
    return user
