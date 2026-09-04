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


@router.post('/token', response_model=Token)
async def login_for_access_token(
    # Um fomulario de login proprio do FastAPI
    session: Session,
    form_data: OAuth2form,
):
    # Usando o email para login
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    # Conferindo se o email existe
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

    # Criando o Token jwt usando o sub email
    access_token = create_access_token({'sub': user.email})

    # Enviando o token
    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: UserT):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'Bearer'}
