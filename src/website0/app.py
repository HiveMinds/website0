"""Hosts a website with a user database stored in MongoDB Atlas.

Allows you to create new users, and login as those users. The passwords
are stored hashed and salted.
"""
import json
import os
from typing import Any, Optional, Tuple, Union

import bcrypt
import flask
from flask import Flask, redirect, render_template, request, session, url_for
from pymongo.cursor import Cursor
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from typeguard import typechecked

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


# Include Mollie.
@app.route("/")  # type: ignore[misc]
def show_list() -> str:
    """Returns html code which can show the list of Mollie examples in body of
    the website."""
    body: str = ""
    # pylint:disable=E0601
    for example in examples:
        body += f'<a href="/{example}">{example}</a><br>'
    return body


@app.route("/<example>", methods=["GET", "POST"])  # type: ignore[misc]
def run_example(example: Optional[str] = None) -> Any:
    """Runs the Mollie example with the given name."""
    print(f"examples={examples}")
    print(f"example={example}")
    if example not in examples:
        flask.abort(404, "Example does not exist")
    # return __import__(example).main()
    print(f"import src.website0.{example}\n\n")
    return __import__(f"src.website0.{example}").main()


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


if __name__ == "__main__":
    examples = [
        "01-new-payment",
        "01-new-payment-using-qrcode",
        "02-webhook-verification",
        "03-return-page",
        "04-ideal-payment",
        "05-payments-history",
        "06-list-activated-methods",
        "07-new-customer",
        "08-list-customers",
        "09-create-customer-payment",
        "10-customer-payment-history",
        "11-refund-payment",
        "12-new-order",
        "13-order-webhook-verification",
        "14-cancel-order",
        "15-list-orders",
        "16-cancel-order-line",
        "17-order-return-page",
        "18-ship-order-completely",
        "19-ship-order-partially",
        "20-get-shipment",
        "21-list-order-shipments",
        "22-refund-order-completely",
        "23-update-shipment-tracking",
    ]

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
