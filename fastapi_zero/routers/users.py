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


# endpoint para ver os usuarios cadastrados
@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    session: Session,
    current_user: Current_user,  # So consegue pesquisar se tiver logado
    filter_user: Annotated[FilterPage, Query()],
):

    # um scalars para retorar todos os user no db usando o filtro Query
    users = await session.scalars(
        select(User).limit(filter_user.limit).offset(filter_user.offset)
    )

    # Como o modelo é um dict, temos re retonar em dict
    return {'users': users}


# Endpoint para procurar user pelo id do Banco de dados
@router.get(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPlublic
)
async def get_user_id(
    user_id: int,
    session: Session,
    current_user: Current_user,  # So consegue pesquisar se tiver logado
):

    # Faz a busca usando o id como parametro
    user_db = await session.scalar(select(User).where(User.id == user_id))

    # Erro caso não encontre o user
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return user_db


# Endpoint para Criar um novo usuario
@router.post(
    '/',  # endpoint, pedaço da url que representa esse pedaço de codigo
    status_code=HTTPStatus.CREATED,  # Retorna 201 - Created
    response_model=UserPlublic,  # Schema de resposta
)
async def create_user(
    user: UserSchema,
    # oque vinher no parametro user é convertido no objeto UserSchema
    session: Session,
):

    # Conferindo se os dados passos iram bater com os campos UNIQUE do db
    response = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    # se o select de cima retornar algo entra no if e manda o erro
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

    # Caso não retorne nada cria um user usando o orm
    response = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    # Commita o user no db
    session.add(response)
    await session.commit()
    await session.refresh(response)

    # retornar o user criado
    return response


# Endpoint para atualizar um novo usuario
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
    # já puxa o user que retorna no login do current_user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    current_user.email = user.email
    current_user.username = user.username
    # alterando a senha limpa recebida para um hash
    current_user.password = get_password_hash(user.password)

    # tentando fazer o commit da trasação
    try:
        session.add(current_user)
        await session.commit()
        await session.refresh(current_user)

        return current_user

    # Caso dê erro de integridade
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User name or Email already exists',
        )


# Endpoint para Deletar um usuario
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

    # Garantir que o usuario so pode alterar sua propria conta
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    # deletando o usuario do db
    await session.delete(current_user)
    await session.commit()

    return {'message': 'User Delete'}
