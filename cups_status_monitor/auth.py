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
from cups_status_monitor.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

"""
Source: https://flask.palletsprojects.com/en/stable/tutorial/views
A Blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application, they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
"""
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.cli.command("register")
@click.option("--email", prompt=True, help="The email of the user.")
@click.password_option(help="The password of the user.")
def register(email, password):
    db = get_db()

    try:
        db.execute(
            "INSERT INTO user (email, password_hash) VALUES (?, ?)",
            (email, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        raise click.ClickException(f"User with email {email} is already registered.")

    click.echo(f"Successfully registered user with email {email}.")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        error = None

        # fetch the user row
        user = db.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            error = "Incorrect email or password."
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
