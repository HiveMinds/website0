"""Hosts a website with a user database stored in MongoDB Atlas.

Allows you to create new users, and login as those users. The passwords
are stored hashed and salted.
"""
import json
from typing import Dict

from typeguard import typechecked


@typechecked
def load_json(file_path: str) -> Dict[str, str]:
    """Load a dictionary from a JSON file.

    Args:
    - file_path (str): The path to the JSON file.

    Returns:
    - dict: The loaded dictionary from the JSON file.
    """
    with open(file_path, encoding="utf-8") as file:
        data: Dict[str, str] = json.load(file)
    return data
