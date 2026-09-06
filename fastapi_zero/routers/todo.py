from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import Todo, User
from fastapi_zero.schemas import (
    FilterTodos,
    Mensagem,
    TodoList,
    TodoPatch,
    TodoPublic,
    TodoSchema,
)
from fastapi_zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

Session = Annotated[AsyncSession, Depends(get_session)]
UserT = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic, status_code=HTTPStatus.CREATED)
async def created_todo(todo: TodoSchema, session: Session, user: UserT):
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(new_todo)
    await session.commit()
    await session.refresh(new_todo)

    return new_todo


@router.get('/', status_code=HTTPStatus.OK, response_model=TodoList)
async def list_todos(
    session: Session, user: UserT, todo_filter: Annotated[FilterTodos, Query()]
):
    query = select(Todo).where(user.id == Todo.user_id)
    # Se no filtro veio um titulo
    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))
        # Ele filtra se a coluna title tem o titulo que veio

    if todo_filter.description:
        query = query.filter(
            Todo.description.contains(todo_filter.description)
        )

    if todo_filter.state:
        query = query.filter(Todo.state.contains(todo_filter.state))

    todos = await session.scalars(
        query.limit(todo_filter.limit).offset(todo_filter.offset)
    )

    return {'todos': todos.all()}


@router.delete(
    '/{todo_id}', status_code=HTTPStatus.OK, response_model=Mensagem
)
async def detele_todo(todo_id: int, user: UserT, session: Session):
    todo = await session.scalar(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
        )

    await session.delete(todo)
    await session.commit()

    return {'message': 'Task has been deleted successfully'}


@router.patch(
    '/{todo_id}', status_code=HTTPStatus.OK, response_model=TodoPublic
)
async def update_todo(
    todo_id: int, user: UserT, session: Session, todo: TodoPatch
):
    db_todo = await session.scalar(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
        )

    # Pega o modelo, transforma em um dict e exclui todo que é None
    # .items, manda uma lista de tuplas chave | valor
    # Nome da chave, Value é o valor que vai pro db
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)
    # Tudo isso para resumir os ifs la de cima, pra ter os dois ex

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo
