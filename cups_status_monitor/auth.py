import functools

import click
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from cups_status_monitor.db import get_db

"""
Source: https://flask.palletsprojects.com/en/stable/tutorial/views
A Blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application, they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
"""
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.cli.command("register")
@click.option("--username", prompt=True, help="The name of the user.")
@click.password_option(help="The password of the user.")
def register(username, password):
    db = get_db()

    try:
        db.execute(
            "INSERT INTO user (username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        raise click.ClickException(
            f"User with username {username} is already registered."
        )

    click.echo(f"Successfully registered user with username {username}.")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        error = None

        # fetch the user row
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            error = "Incorrect username or password."
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("admin.dashboard"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("You are not logged in.")
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
