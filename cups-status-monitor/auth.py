import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from flaskr.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

"""
Source: https://flask.palletsprojects.com/en/stable/tutorial/views
A Blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application, they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
"""
bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM user WHERE email = ?", (email,)
        ).fetchone()