from app.s3 import get_from_s3, upload_to_s3
from tests.conftest import pytestmark
from tests.helper_functions import generate_random_string


@pytestmark
async def test_create_s3_item(client, monkeypatch):
    key = await generate_random_string()
    value = await generate_random_string()

    assert await get_from_s3(key=key) == b''

    response = await client.post(f'/s3/?key={key}&value={value}')
    assert response.status_code == 201

    assert (await get_from_s3(key=key)).decode('utf-8') == value


@pytestmark
async def test_get_s3_item(client, monkeypatch):
    key = await generate_random_string()
    value = await generate_random_string()

    response = await client.get(f'/s3/?key={key}')
    assert response.status_code == 404
    assert response.json() == {"detail": "Could not retrieve item!"}

    await upload_to_s3(file=value.encode('utf-8'), key=key)

    response = await client.get(f'/s3/?key={key}')
    assert response.status_code == 200
    assert response.json() == value


@pytestmark
async def test_update_s3_item(client, monkeypatch):
    key = await generate_random_string()
    value = await generate_random_string()

    await client.post(f'/s3/?key={key}&value={value}')
    assert (await get_from_s3(key=key)).decode('utf-8') == value

    new_value = await generate_random_string()
    response = await client.put(f'/s3/?key={key}&value={new_value}')
    assert response.status_code == 200
    assert (await get_from_s3(key=key)).decode('utf-8') == new_value


@pytestmark
async def test_delete_s3_item(client, monkeypatch):
    key = await generate_random_string()
    value = await generate_random_string()

    await client.post(f'/s3/?key={key}&value={value}')
    assert (await get_from_s3(key=key)).decode('utf-8') == value

    response = await client.delete(f'/s3/?key={key}')
    assert response.status_code == 200
    assert await get_from_s3(key=key) == b''
