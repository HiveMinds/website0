"""Hosts a website with a user database stored in MongoDB Atlas.

Allows you to create new users, and login as those users. The passwords
are stored hashed and salted.
"""
from typing import Any, Tuple, Union

import bcrypt
from flask import Flask, redirect, render_template, request, session, url_for
from pymongo.cursor import Cursor
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.website0.credits import get_credits, set_credits
from src.website0.database_helper import add_user, get_users
from src.website0.helper_environment import load_config

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


@app.route("/buy_credits", methods=["POST"])  # type: ignore[misc]
def buy_credits() -> Tuple[str, int]:
    """Represents the buy credits page of the website."""
    # Call the function to buy credits here
    # Ensure proper error handling and response as needed
    # Example:
    # buy_credits()
    current_redits: int = get_credits(
        some_client=client, username=session["username"]
    )
    print(f"current credits: {current_redits}")
    set_credits(
        some_client=client,
        username=session["username"],
        new_credits=current_redits + 100,
    )
    return (
        "Credits bought successfully",
        200,
    )  # Adjust the response as per your requirements


if __name__ == "__main__":
    app_secret: str
    mongo_uri: str
    app_secret, mongo_uri = load_config()

    # Create a new client and connect to the server
    client = MongoClient(mongo_uri, server_api=ServerApi("1"))

    # Send a ping to confirm a successful connection
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")

    # app.check_credits(some_client=client)
    app.secret_key = app_secret
    app.run(debug=False)
