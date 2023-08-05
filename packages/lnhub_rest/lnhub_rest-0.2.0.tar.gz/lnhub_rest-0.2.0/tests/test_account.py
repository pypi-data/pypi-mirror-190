from lnhub_rest.main import client
from lnhub_rest.routers.account import (
    get_account_by_handle,
    get_account_by_id,
    get_account_instances,
)

account_expected = {
    "id": "29cff183-c34d-445f-b6cf-31fb3b566158",
    "lnid": "DzTjkKse",
    "handle": "testuser1",
    "name": "Test User1",
    "bio": "Test user at Lamin",
    "website": None,
    "github_handle": None,
    "twitter_handle": None,
    "linkedin_handle": None,
    "created_at": "2022-10-07T16:39:58.68071",
    "updated_at": None,
    "user_id": "29cff183-c34d-445f-b6cf-31fb3b566158",
    "avatar_url": None,
}


def test_get_account_by_id():
    account = get_account_by_id("29cff183-c34d-445f-b6cf-31fb3b566158")
    assert str(account) == str(account_expected)


def test_get_account_by_id_rest():
    response = client.get("/account/29cff183-c34d-445f-b6cf-31fb3b566158")
    assert str(response.json()) == str(account_expected)


def test_get_account_by_handle():
    account = get_account_by_handle("testuser1")
    assert str(account) == str(account_expected)


def test_get_account_by_handle_rest():
    response = client.get("/account/handle/testuser1")
    assert str(response.json()) == str(account_expected)


account_instances_expected = [
    {
        "id": "93e590c7-845c-460c-9e41-b075916ea38a",
        "account_id": "0969d757-d1a0-4750-888a-b6fbbaba6103",
        "name": "retro",
        "storage_id": "c633f351-4d73-4c78-b808-1414c742119e",
        "db": "postgresql://batman:robin@35.222.187.204:5432/retro",
        "schema_str": "",
        "created_at": "2023-01-17T09:44:02.155451",
        "updated_at": None,
        "description": None,
        "public": False,
        "account": {
            "handle": "testuser2",
            "id": "0969d757-d1a0-4750-888a-b6fbbaba6103",
        },
    },
    {
        "id": "c33b7e2c-d330-4d58-8148-de8dbbd77599",
        "account_id": "0969d757-d1a0-4750-888a-b6fbbaba6103",
        "name": "ln-retro-sqlite",
        "storage_id": "9011ded9-62ba-4938-8f3f-f9459cd16f12",
        "db": None,
        "schema_str": "",
        "created_at": "2023-01-17T09:44:39.266267",
        "updated_at": None,
        "description": None,
        "public": False,
        "account": {
            "handle": "testuser2",
            "id": "0969d757-d1a0-4750-888a-b6fbbaba6103",
        },
    },
    {
        "id": "b1a1c66e-2004-4580-bdb0-fc295f06986c",
        "account_id": "0969d757-d1a0-4750-888a-b6fbbaba6103",
        "name": "test-streaming",
        "storage_id": "a57cf777-a606-4c72-813e-443163b6c244",
        "db": None,
        "schema_str": "",
        "created_at": "2023-01-23T11:50:31.236124",
        "updated_at": None,
        "description": None,
        "public": False,
        "account": {
            "handle": "testuser2",
            "id": "0969d757-d1a0-4750-888a-b6fbbaba6103",
        },
    },
    {
        "id": "25cf0780-d5a1-4ebe-bb6e-9b06c50c5ee5",
        "account_id": "0969d757-d1a0-4750-888a-b6fbbaba6103",
        "name": "lamin0",
        "storage_id": "3fc43c5e-88aa-440b-866f-70f520efd216",
        "db": None,
        "schema_str": "",
        "created_at": "2023-01-23T15:15:28.550081",
        "updated_at": None,
        "description": None,
        "public": False,
        "account": {
            "handle": "testuser2",
            "id": "0969d757-d1a0-4750-888a-b6fbbaba6103",
        },
    },
    {
        "id": "a8fde460-307f-4bce-8be1-008b07db1b31",
        "account_id": "0969d757-d1a0-4750-888a-b6fbbaba6103",
        "name": "test-upload",
        "storage_id": "a57cf777-a606-4c72-813e-443163b6c244",
        "db": None,
        "schema_str": "",
        "created_at": "2023-02-02T07:33:33.876902",
        "updated_at": None,
        "description": None,
        "public": False,
        "account": {
            "handle": "testuser2",
            "id": "0969d757-d1a0-4750-888a-b6fbbaba6103",
        },
    },
    {
        "id": "9817ae69-3a97-44b3-a874-59d3bcba8795",
        "account_id": "0969d757-d1a0-4750-888a-b6fbbaba6103",
        "name": "lamindb-ci",
        "storage_id": "4bbc4f80-2a2a-404b-b534-7eab733a4765",
        "db": None,
        "schema_str": "",
        "created_at": "2023-02-02T08:44:37.433384",
        "updated_at": None,
        "description": None,
        "public": False,
        "account": {
            "handle": "testuser2",
            "id": "0969d757-d1a0-4750-888a-b6fbbaba6103",
        },
    },
]


def test_get_account_instances():
    instances = get_account_instances("testuser2")
    assert str(instances) == str(account_instances_expected)


def test_get_account_instances_rest():
    response = client.get("/account/resources/owned/instances/testuser2")
    assert str(response.json()) == str(account_instances_expected)
