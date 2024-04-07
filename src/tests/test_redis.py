from tests.conftest import pytestmark
from tests.helper_functions import generate_random_string, get_redis_record, create_random_redis_record


@pytestmark
async def test_create_redis_item(client, monkeypatch):
    key = await generate_random_string()
    value = await generate_random_string()

    assert await get_redis_record(key=key) is None

    response = await client.post(f'/redis/?key={key}&value={value}')
    assert response.status_code == 201

    assert (await get_redis_record(key=key)).decode('utf-8') == value


@pytestmark
async def test_get_redis_item(client, monkeypatch):
    key = await generate_random_string()
    value = await generate_random_string()

    response = await client.get(f'/redis/?key={key}')
    assert response.status_code == 404
    assert response.json() == {"detail": "Could not retrieve item!"}

    await create_random_redis_record(key=key, value=value)

    response = await client.get(f'/redis/?key={key}')
    assert response.status_code == 200
    assert response.json() == value


@pytestmark
async def test_update_redis_item(client, monkeypatch):
    key = await generate_random_string()
    value = await generate_random_string()

    await client.post(f'/redis/?key={key}&value={value}')
    assert (await get_redis_record(key=key)).decode('utf-8') == value

    new_value = await generate_random_string()
    response = await client.put(f'/redis/?key={key}&value={new_value}')
    assert response.status_code == 200
    assert (await get_redis_record(key=key)).decode('utf-8') == new_value


@pytestmark
async def test_delete_redis_item(client, monkeypatch):
    key = await generate_random_string()
    value = await generate_random_string()

    await client.post(f'/redis/?key={key}&value={value}')
    assert (await get_redis_record(key=key)).decode('utf-8') == value

    response = await client.delete(f'/redis/?key={key}')
    assert response.status_code == 200
    assert await get_redis_record(key=key) is None
