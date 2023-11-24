"""Example python file with a function."""
import re

import bcrypt
import bson
from pymongo.cursor import Cursor
from pymongo.mongo_client import MongoClient
from typeguard import typechecked


@typechecked
def get_collection(
    *, some_client: MongoClient, collection_name: str
) -> Cursor:
    """Returns the users from the database."""
    database = some_client["database0"]
    users_collection = database[collection_name]
    # Retrieve all users from the 'users' collection
    users: Cursor = users_collection.find()
    return users


@typechecked
def add_user(
    *, some_client: MongoClient, username: str, password: bytes
) -> bson.objectid.ObjectId:
    """Adds a new username and password to the MongoDB 'users' collection."""
    database = some_client["database0"]
    users_collection = database["users"]

    hashed_salted_pwd = bcrypt.hashpw(password, bcrypt.gensalt())

    # Create a document for the new user
    user_document = {
        "username": username,
        "password": hashed_salted_pwd.decode("utf-8"),
    }

    # Insert the new user document into the 'users' collection
    result = users_collection.insert_one(user_document)

    initialise_zero_credits(some_client=some_client, username=username)

    # Return the ID of the inserted document
    return result.inserted_id


@typechecked
def has_email_format(*, username: str) -> bool:
    """Check if the given username follows the email format.

    Args:
    - username (str): The username to be checked for email format.

    Returns:
    - bool: True if the username matches the email format, False otherwise.
    """
    # Regular expression to verify email format
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    # Check if the username matches the email format using regex
    return bool(re.match(email_regex, username))


@typechecked
def initialise_zero_credits(
    *,
    some_client: MongoClient,
    username: str,
) -> None:
    """Initialise the credits database with zero credits for all users."""

    database = some_client["database0"]
    user_credits_collection = database["user_credits"]

    user_credits_doc = {
        "username": username,
        "credits": 42,
    }

    # Initialise the credits database with zero credits for all users
    user_credits_collection.insert_one(user_credits_doc)
