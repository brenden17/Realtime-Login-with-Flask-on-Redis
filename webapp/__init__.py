# -*- coding: utf-8 -*-
from flask import Flask, g

from flask.ext.login import current_user
from .extensions import lss
from .models import db, mongo, login_manager
from .controllers.user import user_blueprint


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)
    lss.init_app(app)
    
    app.register_blueprint(user_blueprint)

    @app.before_first_request
    def init_request():
        db.create_all()

    @app.before_request
    def before_request():
        g.user = current_user
    
    return app

if __name__ == '__main__':
    app = app = create_app('webapp.config.DevConfig')
    app.run()
