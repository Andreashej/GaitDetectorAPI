from flask import Flask, jsonify, Blueprint
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate  import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from flask_marshmallow import Marshmallow

cors = CORS()

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

bp = Blueprint('api', __name__)
api = Api(bp)

def create_app():
    from app import routes, models

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    ma.init_app(app)
    cors.init_app(app)

    with app.app_context():
        from . import routes, models

        app.register_blueprint(bp)

        return app