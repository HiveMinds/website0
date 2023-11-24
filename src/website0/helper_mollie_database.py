"""Hosts a website with a user database stored in MongoDB Atlas.

Allows you to create new users, and login as those users. The passwords
are stored hashed and salted.
"""
import json
import os
from typing import Any, Union

import flask
from typeguard import typechecked


#
# NOTE: This example uses json files as a "database".
# Please use a real database like MySQL in production.
#
@typechecked
def database_write(my_webshop_id: Union[str, int], data: Any) -> None:
    """Store order-related data for the user in a json file."""
    my_webshop_id = int(my_webshop_id)
    file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "orders",
        f"order-{my_webshop_id}.json",
    )
    with open(file, "w", encoding="utf-8") as database:
        json.dump(data, database)


def database_read(my_webshop_id: Union[str, int]) -> Any:
    """Read the order-related data for the user from a json file."""
    my_webshop_id = int(my_webshop_id)
    file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "orders",
        f"order-{my_webshop_id}.json",
    )
    with open(file, encoding="utf-8") as database:
        return json.load(database)


def get_public_url() -> str:
    """Return the base URL for this application, usable for sending to the
    mollie API.

    This will normally return the flask root url, which points to 'localhost'
    on dev machines. This is fine for limited local tests, but when you want
    to make test payments against the Mollie API, you need an endpoint that is
     reachable from the public internet.

    If the variable `MOLLIE_PUBLIC_URL` is available in the environment, we
    will use that instead of the flask root URL.
    """
    url: str
    try:
        url = os.environ["MOLLIE_PUBLIC_URL"]
    except KeyError:
        url = flask.request.url_root

    if not url.endswith("/"):
        return f"{url}/"
    return url
