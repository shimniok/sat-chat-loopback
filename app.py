import os
from config import create_config
from flask import Flask
from json_parser import dt_fmt


def create_app():

    app = Flask(__name__, instance_relative_config=True)

    with app.app_context():

        from config import create_config
        app.config.from_object(create_config())
        
        from loopback import loopback_bp
        app.register_blueprint(loopback_bp)

        return app
