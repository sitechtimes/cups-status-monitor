import os

import db
from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app(test_config=None):
    # create and configure the application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        DATABASE_URL=os.getenv("DATABASE_URL"),
    )

    if test_config is None:
        # load the instance configuration, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test configuration if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    if not app.config.get("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is missing.")

    from . import app, auth

    db.init_app(app)
    app.register_blueprint(auth.bp)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
