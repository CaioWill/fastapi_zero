from http import HTTPStatus

import factory
import factory.fuzzy
import pytest
from factory import Faker

from fastapi_zero.models import Todo, TodoState


def test_created_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'teste',
            'description': 'teste',
            'state': 'todo',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'title': 'teste',
        'description': 'teste',
        'state': 'todo',
        'id': 1,
    }


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = Faker('text')
    description = Faker('text')
    # ele escolhe randomicamente um dos states
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


@pytest.mark.asyncio
async def test_list_todos_should_return_5_todos(
    session, client, created_user, token
):

    # Arrange -> dados
    expected_todos = 5
    # cria os todos no db para o test
    session.add_all(TodoFactory.create_batch(5, user_id=created_user.id))
    await session.commit()

    # act
    response = client.get(
        '/todos/', headers={'Authorization': f'Bearer {token}'}
    )

    # assert
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_pagination_return_2_todos(
    session, client, created_user, token
):

    # Arrange -> dados
    expected_todos = 2
    # cria os todos no db para o test
    session.add_all(TodoFactory.create_batch(5, user_id=created_user.id))
    await session.commit()

    # act
    # passando o limit e offset diretamente na url
    response = client.get(
        '/todos/?limit=2&offset=1',
        headers={'Authorization': f'Bearer {token}'},
    )

    # assert
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_title_return_2_todos(
    session, client, created_user, token
):

    # Arrange -> dados
    expected_todos = 5
    # cria os todos no db para o test
    session.add_all(
        TodoFactory.create_batch(
            5, user_id=created_user.id, title='test1 todo'
        )
    )
    await session.commit()

    # act
    # passando o title diretamente na url
    response1 = client.get(
        '/todos/?title=test1',
        headers={'Authorization': f'Bearer {token}'},
    )

    # assert
    assert len(response1.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_description_return_2_todos(
    session, client, created_user, token
):

    # Arrange -> dados
    expected_todos = 5
    # cria os todos no db para o test
    session.add_all(
        TodoFactory.create_batch(
            5, user_id=created_user.id, description='description'
        )
    )
    await session.commit()

    # act
    # passando o title diretamente na url
    response1 = client.get(
        '/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    # assert
    assert len(response1.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_state_return_2_todos(
    session, client, created_user, token
):

    # Arrange -> dados
    expected_todos = 5
    # cria os todos no db para o test
    session.add_all(
        TodoFactory.create_batch(
            5, user_id=created_user.id, state=TodoState.draft
        )
    )
    await session.commit()

    # act
    # passando o title diretamente na url
    response1 = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    # assert
    assert len(response1.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_delete_todo_not_found(
    client,
    token,
):
    response = client.delete(
        '/todos/10', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


@pytest.mark.asyncio
async def test_delete_todo(client, token, session, created_user):
    todo = TodoFactory(user_id=created_user.id)
    session.add(todo)
    await session.commit()

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfully'}


@pytest.mark.asyncio
async def test_delete_todo_other_user(
    client, token, session, created_user, other_user
):

    todo_other = TodoFactory(user_id=other_user.id)
    session.add(todo_other)
    await session.commit()

    response = client.delete(
        f'/todos/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


def test_patch_todo_not_found(client, token):
    response = client.patch(
        '/todos/1', json={}, headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


@pytest.mark.asyncio
async def test_patch_todo(client, token, created_user, session):

    todo = TodoFactory(user_id=created_user.id)
    session.add(todo)
    await session.commit()

    response = client.patch(
        f'/todos/{created_user.id}',
        json={'title': 'test'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'test'
