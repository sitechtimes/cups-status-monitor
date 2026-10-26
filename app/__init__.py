import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app(test_config=None):
    # Create and configure the application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # Load the instance configuration, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test configuration if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
