import jsonschema
import pytest
import requests

from utils import load_schema


def test_get_single_resource_successfully():
    url = "https://reqres.in/api/unknown/1"
    schema = load_schema("get_single_resource.json")

    result= requests.get(url)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


@pytest.mark.parametrize('id_', [2, 3])
def test_get_single_resource_id(id_):
    url = f"https://reqres.in/api/unknown/{id_}"

    result = requests.get(url)

    assert result.json()['data']['id'] == id_


def test_get_single_resource_not_found():
    url = f"https://reqres.in/api/unknown/23"

    result = requests.get(url)

    assert result.status_code == 404


def test_list_resource_successfully():
    url = "https://reqres.in/api/unknown"
    schema = load_schema("list_resource.json")

    result = requests.get(url)

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_list_resource_page_parameter():
    page = 2
    url = "https://reqres.in/api/unknown"

    result = requests.get(url, params={"page": page})

    assert result.json()["page"] == page


def test_list_resource_per_page_parameter():
    per_page = 10
    url = "https://reqres.in/api/unknown"

    result = requests.get(
        url=url,
        params={"per_page": per_page}
    )

    assert result.json()["per_page"] == per_page
    assert len(result.json()['data']) == per_page


def test_create_user_successfully():
    url = "https://reqres.in/api/users"
    schema = load_schema("create_user.json")

    result = requests.post(url,
                           json={
                               "name": "Morpheus",
                               "job": "leader"
                           })

    assert result.status_code == 201
    assert result.json()['name'] == 'Morpheus'
    assert result.json()['job'] == 'leader'
    jsonschema.validate(result.json(), schema)


def test_update_user_successfully():
    url = "https://reqres.in/api/users/2"
    schema = load_schema("update_user.json")

    result = requests.put(url,
                          json={
                              "name": "Neo",
                              "job": "Zion resident"
                          })

    assert result.status_code == 200
    assert result.json()['name'] == 'Neo'
    assert result.json()['job'] == 'Zion resident'
    jsonschema.validate(result.json(), schema)


def test_delete_user_successfully():
    url = "https://reqres.in/api/users/1"

    result = requests.delete(url)

    assert result.status_code == 204


def test_register_user_successfully():
    url = "https://reqres.in/api/register"
    schema = load_schema("register_user.json")

    result = requests.post(url,
                           json={
                               "email": "eve.holt@reqres.in",
                               "password": "pistol"
                           })

    assert result.status_code == 200
    jsonschema.validate(result.json(), schema)


def test_register_user_invalid_email():
    url = "https://reqres.in/api/register"
    schema = load_schema("register_user.json")

    result = requests.post(url,
                           json={
                               "email": "eve.com",
                               "password": "pistol"
                           })

    assert result.status_code == 400
    assert result.json()['error'] == 'Note: Only defined users succeed registration'


def test_register_user_missing_password():
    url = "https://reqres.in/api/register"
    schema = load_schema("register_user.json")

    result = requests.post(url,
                           json={
                               "email": "eve.holt@reqres.in"
                           })

    assert result.status_code == 400
    assert result.json()['error'] == 'Missing password'

