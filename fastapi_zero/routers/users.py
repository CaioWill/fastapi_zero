# Dominio expecifico para tratar usuarios
from http import HTTPStatus
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,  # Biblioteca de erros, seria o Exception do python cru
    Query,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    FilterPage,
    Mensagem,
    UserList,
    UserPlublic,
    UserSchema,
)
from fastapi_zero.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(tags=['users'], prefix='/users')
# prefix -> cria um prefixo para todos os enpoins dessa Router

# cria a variavel com o typo e o metadata
Session = Annotated[AsyncSession, Depends(get_session)]
Current_user = Annotated[User, Depends(get_current_user)]


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    session: Session,
    current_user: Current_user,
    filter_user: Annotated[FilterPage, Query()],
):

    users = await session.scalars(
        select(User).limit(filter_user.limit).offset(filter_user.offset)
    )

    # Como o modelo é um dict, temos re retonar em dict
    return {'users': users}


@router.get(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPlublic
)
async def get_user_id(user_id: int, session: Session):

    user_db = await session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return user_db


@router.post(
    '/',  # endpoint, pedaço da url que representa esse pedaço de codigo
    status_code=HTTPStatus.CREATED,  # Retorna 201 - Created
    response_model=UserPlublic,  # Schema de resposta
)
# oque vinher no parametro user é convertido no objeto UserSchema
async def create_user(
    user: UserSchema,
    session: Session,
    # com Depends, sempre que chama ela e exec
):

    # session = get_session() -> dessa for so seria executado a func uma vez

    response = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if response:
        if response.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif response.email == user.email:
            raise HTTPException(
                HTTPStatus.CONFLICT, detail='Email already exixts'
            )

    response = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(response)
    await session.commit()
    await session.refresh(response)

    return response


@router.put(
    '/{user_id}',  # adicionamos a variavel, paramentro da url
    status_code=HTTPStatus.OK,
    response_model=UserPlublic,
)
# HTTP://localhost:8000/users/1 -> 1 é a variavel que definimos o paramentro
async def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: Current_user,
):
    # Garantir que o usuario so pode alterar sua propria conta
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    current_user.email = user.email
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)

    try:
        session.add(current_user)
        await session.commit()
        await session.refresh(current_user)

        return current_user

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User name or Email already exists',
        )


@router.delete(
    '/{user_id}',  # adicionamos a variavel, paramentro da url
    status_code=HTTPStatus.OK,
    response_model=Mensagem,
)
async def delete_user(
    user_id: int,
    session: Session,
    current_user: Current_user,
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    await session.commit()

    return {'message': 'User Delete'}
