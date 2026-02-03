from flask import Flask
from shrimp import stories, cli, accounts
from shrimp.utils import db
from shrimp.utils.filters import time_ago

from config import Config


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.cli.add_command(cli.init)
    app.jinja_env.filters["time_ago"] = time_ago

    app.register_blueprint(stories.blueprint)
    app.register_blueprint(accounts.blueprint)
    app.add_url_rule("/", endpoint="home", view_func=stories.routes.index)
    app.teardown_appcontext(db.close_connection)

    return app
