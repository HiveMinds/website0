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
def get_credits(
    *, some_client: MongoClient, username: str  # type: ignore[type-arg]
) -> int:
    """Retrieve the number of credits for a given username."""
    database = some_client["database0"]
    credits_collection = database["user_credits"]

    # Find the user's credit information
    user_credit_info = credits_collection.find_one({"username": username})

    if user_credit_info:
        return int(user_credit_info.get("credits", 0))
    return 0  # Return 0 if user doesn't exist or has no credits


@typechecked
def set_credits(
    *,
    some_client: MongoClient,  # type: ignore[type-arg]
    username: str,
    new_credits: int,
) -> int:
    """Retrieve the number of credits for a given username.

    TODO: change getting username and password using find_one as it is faster.
    """

    old_credits: int = 0
    user_credits_collection = some_client["database0"]["user_credits"]
    user_credit = user_credits_collection.find_one({"username": username})

    if user_credit:
        if "credits" in user_credit:
            old_credits = user_credit["credits"]

        # Update the credits for the user
        user_credits_collection.update_one(
            {"username": username}, {"$set": {"credits": new_credits}}
        )
        print(f"Changed:{old_credits} to: {new_credits}")
        return new_credits

    print(f"Error, was not able to find user_id:{username}")
    return 0  # Return 0 if user doesn't exist or has no credits
