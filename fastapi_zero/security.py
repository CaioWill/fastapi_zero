from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.settings import Settings

# Checa o head e ver se tem um bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

# Descite o melhor tipo de hash
pwd_context = PasswordHash.recommended()

settings = Settings()


# Faz a criptografia da senha em hash
def get_password_hash(password: str):
    return pwd_context.hash(password)


# comparação de hash
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


# func para Autenticar o login e usuarios existem
async def get_current_user(
    session: AsyncSession = Depends(get_session),
    # Garante que um token foi enviado
    token: str = Depends(oauth2_scheme),
):
    # Constant de erro
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Cloud not validate credentials',
        headers={'WWW-Autheticate': 'Bearer'},
    )

    try:
        # Descodando o TOKEN jwt
        playload = decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )

        # Pega o email do playload
        subject_email = playload.get('sub')

        # Garatir que o email veio no sub
        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    # confere que o email esta no db
    user = await session.scalar(
        select(User).where(User.email == subject_email)
    )

    # Se o email nao estiver no db
    if not user:
        raise credentials_exception

    return user
