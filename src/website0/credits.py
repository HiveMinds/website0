"""Example python file with a function."""
from pymongo.mongo_client import MongoClient
from typeguard import typechecked


@typechecked
def add_two(*, x: int) -> int:
    """Adds a value to an incoming number.

    Preserved for testing.
    """
    return x + 2


@typechecked
def get_credits(*, some_client: MongoClient, username: str) -> int:
    """Retrieve the number of credits for a given username."""
    database = some_client["credits_database"]
    credits_collection = database["credits"]

    # Find the user's credit information
    user_credit_info = credits_collection.find_one({"username": username})

    if user_credit_info:
        return int(user_credit_info.get("credits", 0))
    return 0  # Return 0 if user doesn't exist or has no credits
