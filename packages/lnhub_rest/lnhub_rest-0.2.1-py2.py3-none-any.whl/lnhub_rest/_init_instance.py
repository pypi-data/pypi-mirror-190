"""Initializing an instance.

This functionality will at first only be accessible through Python API client & CLI.

We might also enable it from the UI.
"""
from typing import Optional
from uuid import uuid4

from pydantic import PostgresDsn

from lnhub_rest._add_storage import add_storage
from lnhub_rest._assets import schemas as known_schema_names
from lnhub_rest._sbclient import connect_hub_with_auth


def init_instance(
    *,
    owner: str,  # owner handle
    name: str,  # instance name
    storage: str,  # storage location on cloud
    db: Optional[PostgresDsn] = None,  # DB URI
    schema: Optional[str] = None,  # comma-separated list of schema names
):
    hub = connect_hub_with_auth()
    try:
        # get account
        data = hub.table("account").select("*").eq("handle", owner).execute().data
        account = data[0]

        # get storage and add if not yet there
        storage_id = add_storage(storage, account_handle=account["handle"])

        # validate schema arg
        schema_str = validate_schema_arg(schema)

        response = (
            hub.table("instance")
            .select("*")
            .eq("account_id", account["id"])
            .eq("name", name)
            .execute()
        )
        if len(response.data) > 0:
            hub.auth.sign_out()
            return "instance-exists-already"

        instance_id = uuid4().hex

        instance_fields = {
            "id": instance_id,
            "account_id": account["id"],
            "name": name,
            "storage_id": storage_id,
            "db": db,
            "schema_str": schema_str,
        }
        data = hub.table("instance").insert(instance_fields).execute().data
        assert len(data) == 1

        account_instance_fields = {
            "instance_id": instance_id,
            "account_id": account["id"],
            "permission": "admin",
        }
        data = (
            hub.table("account_instance").insert(account_instance_fields).execute().data
        )
        assert len(data) == 1
    finally:
        hub.auth.sign_out()
        return None


def validate_schema_arg(schema: Optional[str] = None) -> str:
    if schema is None:
        return ""
    validated_schema = []
    for module in known_schema_names:
        if module in schema:
            validated_schema.append(module)
    if len(validated_schema) == 0:
        raise ValueError(f"Unknown schema modules. Only know {known_schema_names}.")
    return ",".join(validated_schema)
