from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,  # Biblioteca de erros, seria o Exception do python cru
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import Token
from fastapi_zero.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])

Session = Annotated[AsyncSession, Depends(get_session)]
UserT = Annotated[User, Depends(get_current_user)]

OAuth2form = Annotated[OAuth2PasswordRequestForm, Depends()]


# Endpoint para criação do token - Login
@router.post('/token', response_model=Token)
async def login_for_access_token(
    session: Session,
    # Um fomulario de login ja feito do FastAPI
    form_data: OAuth2form,
):
    # Buscando o email que veio do formulario no db
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )  # Mo formulario vem como username
    # Mas a gente oque vai usar

    # Conferindo se o email existe no db
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    # Conferindo se a hash da senha bate com o hash do banco
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    # Criando o Token jwt enviando o sub
    access_token = create_access_token({'sub': user.email})

    # Enviando o token criado
    return {'access_token': access_token, 'token_type': 'Bearer'}


# Endpoint para atualizar o token
@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: UserT):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'Bearer'}
