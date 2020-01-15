from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

from .resources.UserAPI import UserResource, UsersResource

from .config import config_by_name

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    api = Api(app)
    api.add_resource(UsersResource, '/users')
    api.add_resource(UserResource, '/user/<public_id>')

    db.init_app(app)

    return app
