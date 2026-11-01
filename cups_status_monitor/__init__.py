import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app(test_config=None):
    # create and configure the application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        DATABASE=os.path.join(app.instance_path, "cups-status-monitor.sqlite"),
    )

    if test_config is None:
        # load the instance configuration, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test configuration if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from . import db

    db.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp)

    return app
