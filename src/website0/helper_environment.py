"""Hosts a website with a user database stored in MongoDB Atlas.

Allows you to create new users, and login as those users. The passwords
are stored hashed and salted.
"""
import os
from typing import Dict, Tuple

from src.website0.helper_file import load_json


def set_env_variable(env_var_name: str, variable_value: str) -> None:
    """Set an environment variable and prompt for user input.

    Args:
    - env_var_name: Name of the environment variable
    - variable_value: Value to set for the environment variable

    Returns:
    - user_input: Input provided by the user
    """
    os.environ[env_var_name] = variable_value

    if os.environ.get(env_var_name) != variable_value:
        raise ValueError(
            f"Environment variable {env_var_name} not set correctly"
        )


def load_config() -> Tuple[str, str]:
    """Load the config file from the root directory."""
    # Load config dict from file above root dir.
    config: Dict[str, str] = load_json("../config.yml")
    mongo_username = config["mongodb_username"]
    mongo_pwd = config["mongodb_password"]
    mongo_cluster_name = config["mongodb_cluster_name"]
    mongo_db_name = config["mongodb_database_name"]
    app_secret = config["app_cookie_secret"]
    mollie_test_api_key = config["mollie_test_api_key"]

    # Get the ngrok url.
    ngrok_url: str
    if "ngrok_url" in config.keys():
        ngrok_url = config["ngrok_url"]
    else:
        ngrok_url = input(
            "What is the ngrok https URL? (press enter to continue) "
        )

    # Validate url format.
    if not ngrok_url.startswith("https://"):
        raise ValueError("ngrok URL not valid")
    set_env_variable(
        env_var_name="MOLLIE_PUBLIC_URL", variable_value=ngrok_url
    )

    # Set the Mollie API key as environment variable.
    set_env_variable(
        env_var_name="MOLLIE_API_KEY", variable_value=mollie_test_api_key
    )

    # Load the username from the environment.
    mongo_uri: str = (
        f"mongodb+srv://{mongo_username}:{mongo_pwd}@{mongo_cluster_name}."
        + f"{mongo_db_name}.mongodb.net/?retryWrites=true&w=majority"
    )

    return app_secret, mongo_uri
