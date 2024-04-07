import json
import uuid

import sqlalchemy

from app.models.user import User
from tests.conftest import pytestmark


@pytestmark
async def test_user_add(client, session, monkeypatch):
    statement = sqlalchemy.select(sqlalchemy.func.count()).select_from(User)
    results = await session.exec(statement=statement)
    assert results.scalar_one_or_none() == 0

    response = await client.post('/user/', data=json.dumps({"first_name": "John", "last_name": "Smith"}))
    assert response.status_code == 201

    statement = sqlalchemy.select(sqlalchemy.func.count()).select_from(User).where(User.first_name == "John",
                                                                                   User.last_name == "Smith")
    results = await session.exec(statement=statement)
    assert results.scalar_one_or_none() == 1

    statement = sqlalchemy.select(User).where(User.first_name == "John", User.last_name == "Smith")
    results = await session.exec(statement=statement)
    user = results.scalars().one()
    assert user.first_name == "John"
    assert user.last_name == "Smith"
    assert user.color_theme == "light"

    statement = sqlalchemy.select(sqlalchemy.func.count()).select_from(User)
    results = await session.exec(statement=statement)
    assert results.scalar_one_or_none() == 1


@pytestmark
async def test_user_get(client, session, monkeypatch):
    response = await client.post('/user/', data=json.dumps({"first_name": "John", "last_name": "Smith"}))
    user_id = response.json()["user_id"]

    response = await client.get('/user/?user_id=' + str(user_id))
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
    assert response.json()["last_name"] == "Smith"
    assert response.json()["color_theme"] == "light"

    # Search for a non-existing user
    response = await client.get('/user/?user_id=' + str(uuid.uuid4()))
    assert response.status_code == 404
    assert response.json() == {"detail": "Could not retrieve user!"}


@pytestmark
async def test_user_get_all(client, session, monkeypatch):
    await client.post('/user/', data=json.dumps({"first_name": "John", "last_name": "Smith"}))
    await client.post('/user/', data=json.dumps({"first_name": "Alice", "last_name": "Griffith"}))

    response = await client.get('/user/all')
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytestmark
async def test_user_put(client, session, monkeypatch):
    response = await client.post('/user/', data=json.dumps({"first_name": "John", "last_name": "Smith"}))
    user_id = response.json()["user_id"]

    response = await client.put('/user/?user_id=' + str(user_id), data=json.dumps({"first_name": "Johnny", "last_name": "Smith", "color_theme": "dark"}))
    assert response.status_code == 200
    assert response.json()["first_name"] == "Johnny"
    assert response.json()["last_name"] == "Smith"
    assert response.json()["color_theme"] == "dark"

    statement = sqlalchemy.select(User).where(User.user_id == user_id)
    results = await session.exec(statement=statement)
    user = results.scalars().one()
    assert user.first_name == "Johnny"
    assert user.last_name == "Smith"
    assert user.color_theme == "dark"

    # Modify a non-existing user
    response = await client.put('/user/?user_id=' + str(uuid.uuid4()), data=json.dumps({"first_name": "Johnny", "last_name": "Smith", "color_theme": "dark"}))
    assert response.status_code == 404
    assert response.json() == {"detail": "Could not retrieve user!"}


@pytestmark
async def test_user_delete(client, session, monkeypatch):
    response = await client.post('/user/', data=json.dumps({"first_name": "John", "last_name": "Smith"}))
    user_id = response.json()["user_id"]

    statement = sqlalchemy.select(sqlalchemy.func.count()).select_from(User)
    results = await session.exec(statement=statement)
    assert results.scalar_one_or_none() == 1

    response = await client.delete('/user/?user_id=' + str(user_id))
    assert response.status_code == 200

    statement = sqlalchemy.select(sqlalchemy.func.count()).select_from(User)
    results = await session.exec(statement=statement)
    assert results.scalar_one_or_none() == 0

    # Delete a non-existing user
    response = await client.delete('/user/?user_id=' + str(uuid.uuid4()))
    assert response.status_code == 404
    assert response.json() == {"detail": "Could not retrieve user!"}
