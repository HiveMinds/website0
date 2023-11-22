"""Hosts a website with a user database stored in MongoDB Atlas.

Allows you to create new users, and login as those users. The passwords
are stored hashed and salted.
"""
from typing import Any, Dict, Union

import bcrypt
from flask import Flask, redirect, render_template, request, session, url_for
from pymongo.cursor import Cursor
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.website0.credits import get_credits
from src.website0.database_helper import add_user, get_users
from src.website0.helper_file import load_json

# Start website
app: Flask = Flask(__name__)


@app.route("/")  # type: ignore[misc]
def index() -> Union[Any, str]:
    """Represents the start/index page of the websites.

    Users can login here, or are logged in already.
    """
    if "username" in session:
        return redirect(url_for("dashboard"))

    return render_template("index.html")


@app.route("/login", methods=["POST"])  # type: ignore[misc]
def login() -> Union[Any, str]:
    """Represents the login page of the website."""
    # Get the username from the website form.
    entered_username: str = request.form["username"]

    # Get the users from the database.
    users: Cursor = get_users(some_client=client)

    for user_db in users:
        if user_db["username"] == entered_username:
            user_pwd: bytes = user_db["password"].encode("utf-8")
            if bcrypt.checkpw(request.form["pass"].encode("utf-8"), user_pwd):
                session["username"] = request.form["username"]
                return redirect(url_for("index"))
    return "Invalid username or password"


@app.route("/register", methods=["POST", "GET"])  # type: ignore[misc]
def register() -> Union[Any, str]:
    """Represents the register page of the website.

    Users can create new accounts here.
    """
    if request.method == "POST":
        # Get the username from the website form.
        entered_username: str = request.form["username"]

        # Get the users from the database.
        users: Cursor = get_users(some_client=client)

        # Check if one can create the requested new user by checking if the
        # username does not yet exist.
        for user_db in users:
            if user_db["username"] == entered_username:
                return "That username already exists!"

        # Add the new user to the database.
        add_user(
            some_client=client,
            username=entered_username,
            password=request.form["pass"].encode("utf-8"),
        )
        return redirect(url_for("index"))
    return render_template("register.html")


@app.route("/dashboard")  # type: ignore[misc]
def dashboard() -> Union[Any, str]:
    """Renders the dashboard with the user's credits."""
    if "username" not in session:
        return render_template("index.html")
    username: str = session["username"]
    remaining_credits: int = get_credits(some_client=client, username=username)
    print(f"user {username} has {remaining_credits} credits")
    return render_template(
        "dashboard.html",
        username=username,
        remaining_credits=remaining_credits,
    )


if __name__ == "__main__":
    # Load config dict from file above root dir.
    config: Dict[str, str] = load_json("../config.yml")
    mongo_username = config["mongodb_username"]
    mongo_pwd = config["mongodb_password"]
    mongo_cluster_name = config["mongodb_cluster_name"]
    mongo_db_name = config["mongodb_database_name"]
    app_secret = config["app_cookie_secret"]

    # Load the username from the environment.
    mongo_uri: str = (
        f"mongodb+srv://{mongo_username}:{mongo_pwd}@{mongo_cluster_name}."
        + f"{mongo_db_name}.mongodb.net/?retryWrites=true&w=majority"
    )

    # Create a new client and connect to the server
    client = MongoClient(mongo_uri, server_api=ServerApi("1"))

    # Send a ping to confirm a successful connection
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")

    # app.check_credits(some_client=client)
    app.secret_key = app_secret
    app.run(debug=False)
